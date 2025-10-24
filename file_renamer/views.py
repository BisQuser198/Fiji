from django.shortcuts import render

# Create your views here.
# file_renamer/views.py

import os
import io
import zipfile

from django.shortcuts import render
from django.http import HttpResponse
from .forms import RenameForm

def mass_rename(request):
    # View for handling form submission and file renaming.
    # What it does: Renders form on GET; processes zip, generates new names, returns new zip on POST.
    # How it does it: Validates form, extracts zip files, generates bases per mode, creates new zip in memory.
    
    if request.method == 'POST':
        form = RenameForm(request.POST, request.FILES)
        if form.is_valid():
            zip_bytes = request.FILES['zip_file'].read()  # zip_file = forms.FileField() in forms.py called by {% for field in form %} in mass_rename.html
            zip_io = io.BytesIO(zip_bytes)
            try:
                z = zipfile.ZipFile(zip_io)
            except zipfile.BadZipFile:
                form.add_error('zip_file', 'Invalid zip file.')
                return render(request, 'file_renamer/mass_rename.html', {'form': form})
            
            file_list = [] # list of file names in zip
            for f in z.namelist():
                if not f.endswith('/') and not f.startswith('__MACOSX/'):
                    file_list.append(f)
            file_list.sort()
            num_files = len(file_list)
            if num_files == 0: # check if zip has no files
                form.add_error('zip_file', 'Zip contains no files.')
                z.close()
                return render(request, 'file_renamer/mass_rename.html', {'form': form})
            
            mode = form.cleaned_data['mode']
            new_bases = []
            if mode == 'basic': # select basic vs custom mode
                root = form.cleaned_data['root_label'] # extract parameters from form
                use_pre = form.cleaned_data['use_prefix']
                use_suf = form.cleaned_data['use_suffix']
                start = form.cleaned_data['start_num']
                end = form.cleaned_data['end_num']
                if end is None:
                    end = start + num_files - 1
                if end < start:
                    form.add_error('end_num', 'End must be >= start.')
                    z.close()
                    return render(request, 'file_renamer/mass_rename.html', {'form': form}) # extracted parameters from form
                calc_count = end - start + 1
                if calc_count != num_files:
                    form.add_error('end_num', f'Range {start}-{end} covers {calc_count} items, but zip has {num_files} files.')
                    z.close()
                    return render(request, 'file_renamer/mass_rename.html', {'form': form})
                # generate new names
                for i in range(num_files):
                    num_str = str(start + i)
                    parts = []
                    if use_pre: # if prefix checkbox is checked
                        parts.append(num_str)
                    parts.append(root)
                    if use_suf: # if suffix checkbox is checked
                        parts.append(num_str)
                    new_base = ''.join(parts)
                    new_bases.append(new_base)
            else:  # custom rule
                custom_rule = form.cleaned_data['custom_rule']
                groups = []
                total_count = 0
                line_num = 1
                error = False
                for line in custom_rule.splitlines():
                    if line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) != 3:
                            form.add_error('custom_rule', f'Invalid format in line {line_num}: expected text,start,end.')
                            error = True
                            break
                        text = parts[0]
                        try:
                            fr = int(parts[1])
                            to = int(parts[2])
                            if to < fr:
                                raise ValueError
                            count = to - fr + 1
                            total_count += count
                            groups.append((text, fr, to))
                        except ValueError:
                            form.add_error('custom_rule', f'Invalid numbers in line {line_num}.')
                            error = True
                            break
                    line_num += 1
                if error:
                    z.close()
                    return render(request, 'file_renamer/mass_rename.html', {'form': form})
                if total_count != num_files:
                    form.add_error('custom_rule', f'Total names from rules: {total_count}, but zip has {num_files} files.')
                    z.close()
                    return render(request, 'file_renamer/mass_rename.html', {'form': form})
                # for text, fr, to in groups:
                #     for n in range(fr, to + 1):
                #         new_base = text + str(n)
                #         new_bases.append(new_base)

                if len(groups) == 2:
                    text1, fr1, to1 = groups[0]
                    text2, fr2, to2 = groups[1]
                    for i in range(fr1, to1 + 1):
                        for j in range(fr2, to2 + 1):
                            new_base = f"{text1}{i} {text2}{j}"
                            new_bases.append(new_base)
                else:
                    # fallback to old logic for other cases
                    for text, fr, to in groups:
                        for n in range(fr, to + 1):
                            new_base = text + str(n)
                            new_bases.append(new_base)
            
            # Check for potential duplicate names.
            new_names_set = set()
            duplicate = False
            for i in range(num_files):
                ext = os.path.splitext(file_list[i])[1]
                new_name = new_bases[i] + ext
                if new_name in new_names_set:
                    form.add_error(None, f'Duplicate file name generated: {new_name}')
                    duplicate = True
                    break
                new_names_set.add(new_name)
            if duplicate:
                z.close()
                return render(request, 'file_renamer/mass_rename.html', {'form': form})
            
            # Create new zip in memory.
            output_io = io.BytesIO() # is an in-memory byte buffer.
            new_z = zipfile.ZipFile(output_io, mode='w', compression=zipfile.ZIP_DEFLATED)
            for i, orig_path in enumerate(file_list):
                f_in = z.open(orig_path)
                data = f_in.read()
                f_in.close()
                ext = os.path.splitext(orig_path)[1]
                new_name = new_bases[i] + ext
                new_z.writestr(new_name, data)
            new_z.close()
            z.close()
            
            # Prepare HTTP response.
            output_io.seek(0)
            zip_content = output_io.read()
            response = HttpResponse(zip_content, content_type='application/zip') # wrap in HTTP response
            response['Content-Disposition'] = 'attachment; filename="renamed.zip"'
            return response # if form is valid return response = HTTPResponse(zip_content, content_type='application/zip')
# Response flow: Request --> view --> HttpResponse --> Client / Browser
# browser sets POST request to django url, which dispatches to mass_rename view, which returns the HttPResponse (the response = HttpResponse)
# Django’s server stack (framework internals) send back the HttpResponse to the client. 
# Client receives the HTTP response; BECAUSE THE CONTENT HAS Content--Disposition: and content_type='application/zip', the browser 
# opens a dialog box to save the zip.
# Nothing in forms.py or mass_rename.html “receives” the HttpResponse. The django framework delivers the response to the user.
    else:
        form = RenameForm()
    
    return render(request, 'file_renamer/mass_rename.html', {'form': form})