# Create Slides 
# John Roy Daradal

# TODO: MAKE EVERYTHING OBJECT-ORIENTED!!!!!
import os,sys
slide_name = ""

class Token(object):
    def __init__(self,value,token_type):
        self.value = value
        self.type = token_type
    def __str__(self):
        return self.value

HEADER = 1
SLIDES = 2

TITLE = 'Title'
TITLE_CENTER = 'Title_Center'
DL = 'DL'
DT = 'DT'
DD = 'DD'
UL = 'UL'
OLA = 'OLA'
OLN = 'OLN'
OLIN = 'OLIN'
OLIA = 'OLIA'
ULI = 'ULI'
OPEN_DIV = 'ODIV'
CLOSE_DIV = 'CDIV'
HTML = 'HTML'
P = 'P'
IMG = 'IMG'
VID = 'VID'
def get_list_end_tag(list_type):
    if list_type == UL:
        return '</ul>'
    elif list_type == OLN or list_type == OLA:
        return '</ol>'
    elif list_type == DL:
        return '</dl>'
    else:
        return None
def indent(slide_token):
    slide,token_type = slide_token.value,slide_token.type
    offset = 2
    level = 0
    if token_type == TITLE:
        level = 1
    elif token_type == TITLE_CENTER:
        level = 1
    elif token_type == DL:
        level = 1
    elif token_type == DT:
        level = 2
    elif token_type == DD:
        level = 3
    elif token_type == OLN:
        level = 1
    elif token_type == OLA:
        level = 1
    elif token_type == UL:
        level = 1
    elif token_type == OLIN:
        level = 2
    elif token_type == OLIA:
        level = 2
    elif token_type == ULI:
        level = 2
    elif token_type == IMG:
        level = 1
    elif token_type == VID:
        level = 1
    elif token_type == P:
        level = 1
        
    level += offset
    return '\t'*level + slide
def process_header_data(line):
    return [x.strip() for x in line.split(':',1)]
def process_slides(slides):
    processed = []
    last_list = None

    open_dl_tag = indent(Token('<dl>',DL))
    open_div_tag = indent(Token('<section>',OPEN_DIV))
    close_div_tag = indent(Token('</section>',CLOSE_DIV))
    open_oln_tag = indent(Token('<ol class="num">',OLN))
    open_ola_tag = indent(Token('<ol class="alpha">',OLA))
    open_ul_tag = indent(Token('<ul>',UL))

    for i,slide_token in enumerate(slides):
        slide,token_type = slide_token.value,slide_token.type
        if token_type == TITLE or token_type == TITLE_CENTER:
            if i == 0:
                processed.append(open_div_tag)
                processed.append(indent(slide_token))
            else:
                list_end_tag = get_list_end_tag(last_list)
                if list_end_tag:
                    end_tag_token = Token(list_end_tag,last_list)
                    processed.append(indent(end_tag_token))
                    last_list = None   
                processed.append(close_div_tag)
                processed.append(open_div_tag)
                processed.append(indent(slide_token))
        elif token_type == DT:
            list_end_tag = get_list_end_tag(last_list)
            if list_end_tag and last_list != DL:
                end_tag_token = Token(list_end_tag,last_list)
                processed.append(indent(end_tag_token))
                last_list = None
            if last_list is None:
                last_list = DL
                processed.append(open_dl_tag)
            processed.append(indent(slide_token))  
        elif token_type == DD:
            processed.append(indent(slide_token))
        elif token_type == OLIN:
            list_end_tag = get_list_end_tag(last_list)
            if list_end_tag and last_list != OLN:
                end_tag_token = Token(list_end_tag,last_list)
                processed.append(indent(end_tag_token))
                last_list = None
            if last_list is None:
                last_list = OLN
                processed.append(open_oln_tag)
            processed.append(indent(slide_token))  
        elif token_type == OLIA:
            list_end_tag = get_list_end_tag(last_list)
            if list_end_tag and last_list != OLA:
                end_tag_token = Token(list_end_tag,last_list)
                processed.append(indent(end_tag_token))
                last_list = None
            if last_list is None:
                last_list = OLA
                processed.append(open_ola_tag)
            processed.append(indent(slide_token)) 
        elif token_type == ULI:
            list_end_tag = get_list_end_tag(last_list)
            if list_end_tag and last_list != UL:
                end_tag_token = Token(list_end_tag,last_list)
                processed.append(indent(end_tag_token))
                last_list = None
            if last_list is None:
                last_list = UL
                processed.append(open_ul_tag)
            processed.append(indent(slide_token))  
            
        else:
            processed.append(indent(slide_token))
    
    #closing div tag for last slide
    list_end_tag = get_list_end_tag(last_list)
    if list_end_tag:
        end_tag_token = Token(list_end_tag,last_list)
        processed.append(indent(end_tag_token))
        last_list = None
    processed.append(close_div_tag)

    return '\n'.join(processed)
def get_slide_contents(source_file):
    if not os.path.exists(source_file):
        print('Error: {filename} does not exist.'.format(filename=source_file))
        sys.exit()

    f = open(source_file,'r')
    lines = f.readlines()
    f.close()

    current_state = None
    data = {}
    slides = []
    mode = 'normal'

    for line in lines:
        isFragment = False
        if mode != 'code':
            line = line.strip()
            if line.startswith('>'):
                line = line.lstrip('>').strip()
                isFragment = True

        if line == '(header)':
            current_state = HEADER
        elif line == '(slides)':
            current_state = SLIDES
        elif current_state == HEADER:
            key, value = process_header_data(line)
            data[key] = value
        elif current_state == SLIDES:

            if line.startswith('(code)'):
                klass = ['block']
                if 'smaller' in line:
                    klass.append('smaller')
                if 'nocenter' in line:
                    klass.append('nocenter')
                if 'objectivec' in line:
                    klass.append('objectivec')
                klass = ' '.join(klass)
                if isFragment: klass += ' fragment'
                slide_token = Token('<pre><code class="%s">' % klass,HTML)
                slides.append(slide_token)
                mode = 'code'
            elif line.strip().startswith('(endcode)'):
                slide_token = Token('</code></pre>',HTML)
                slides.append(slide_token)
                mode = 'normal'
            elif mode == 'code':
                #as-is
                line = line.replace('<','&lt;').replace('>','&gt;').replace(' ','&nbsp;')
                #slide_token = Token(line + "<br/>",HTML)
                slide_token = Token(line,HTML)
                slides.append(slide_token)
            elif line.startswith('++'):
                #center title => h1.center
                text = line.lstrip('+ ')
                klass = "center"
                if isFragment: klass += ' fragment'
                slide_token = Token('<h2 class="{klass}"><span>{text}</span></h2>'.format(text=text,klass=klass),TITLE_CENTER)
                slides.append(slide_token)
            elif line.startswith('+-'):
                text = line.lstrip('+- ')
                klass = ''
                if isFragment: klass = 'fragment'
                slide_token = Token('<h2 class="{klass}"><small>{text}</small></h2>'.format(text=text,klass=klass),TITLE_CENTER)
                slides.append(slide_token)
            elif line.startswith('+'):
                #title => h1
                text = line.lstrip('+ ')
                klass = ''
                if isFragment: klass = 'fragment'
                slide_token = Token('<h2 class="{klass}">{text}</h2>'.format(text=text,klass=klass),TITLE)
                slides.append(slide_token)
            elif line.startswith('q:'):
                text = line.strip()[2:].lstrip()
                klass = ''
                if isFragment: klass = 'fragment'
                slide_token = Token('<blockquote class="{klass}">"{text}"</blockquote>'.format(text=text,klass=klass),P)
                slides.append(slide_token)
            elif line.startswith(':'):
                #dt
                text = line.lstrip(': ')
                klass = ''
                if isFragment: klass = 'fragment'
                slide_token = Token('\t<dt class="{klass}">{text}</dt>'.format(text=text,klass=klass),DT)
                slides.append(slide_token)
            elif line.startswith('-'):
                #dd
                text = line.lstrip('- ')
                klass = ''
                if isFragment: klass = 'fragment'
                slide_token = Token('\t\t<dd class="{klass}">{text}</dd>'.format(text=text,klass=klass),DD)
                slides.append(slide_token)
            elif line.startswith('#'):
                #ol with number
                text = line.lstrip('# ')
                klass = ''
                if isFragment: klass = 'fragment'
                slide_token = Token('\t<li class="{klass}">{text}</li>'.format(text=text,klass=klass),OLIN)
                slides.append(slide_token)
            elif line.startswith('@'):
                #ol with alphabet
                text = line.lstrip('@ ')
                klass = ''
                if isFragment: klass = 'fragment'
                slide_token = Token('\t<li class="{klass}">{text}</li>'.format(text=text,klass=klass),OLIA)
                slides.append(slide_token)
            elif line.startswith('*'):
                #ul
                text = line.lstrip('* ')
                klass = ''
                if isFragment: klass = 'fragment'
                slide_token = Token('\t<li class="{klass}">{text}</li>'.format(text=text,klass=klass),ULI)
                slides.append(slide_token)
            elif line.startswith("<"):
                #html tags
                # TODO: how to add fragment?
                slide_token = Token(line,HTML)
                slides.append(slide_token)
            elif line.startswith('img:'):
                text = line[4:].strip()
                subj,lec = slide_name.split('_')

                klass = ''
                if isFragment: klass = 'fragment'
                d = {'text':text, 'subj':subj,'lec':lec,'klass':klass}
                slide_token = Token('<img class="{klass}" src="img/{subj}/{lec}/{text}" />'.format(**d),IMG)
                slides.append(slide_token)
            elif line.startswith('img_height='):
                text = line.split(':')[1].strip()
                height = line.split(':')[0].split('=')[1].strip()
                subj,lec = slide_name.split('_')

                klass = ''
                if isFragment: klass = 'fragment'
                d = {'text': text, 'subj': subj, 'lec': lec,'klass':klass, 'height':height}
                slide_token = Token('<img class="{klass}" src="img/{subj}/{lec}/{text}" height="{height}" />'.format(**d),IMG)
                slides.append(slide_token)
            elif line.startswith('img_right:'):
                text = line[10:].strip()
                subj,lec = slide_name.split('_')

                d = {'text':text, 'subj':subj,'lec':lec,'klass':'float_right'}
                slide_token = Token('<img class="{klass}" src="img/{subj}/{lec}/{text}" />'.format(**d),IMG)
                slides.append(slide_token)
            elif line.startswith('img_noborder:'):
                text = line[13:].strip()
                subj,lec = slide_name.split('_')

                klass = 'noborder'
                if isFragment: klass += ' fragment'
                d = {'text':text, 'subj':subj,'lec':lec,'klass':klass}
                slide_token = Token('<img class="{klass}" src="img/{subj}/{lec}/{text}" />'.format(**d),IMG)
                slides.append(slide_token)
            elif line.startswith('video_height='):
                text = line.split(':')[1].strip()
                height = line.split(':')[0].split('=')[1].strip()
                subj,lec = slide_name.split('_')

                klass = ''
                if isFragment: klass = 'fragment'
                d = {'text':text, 'subj':subj,'lec':lec,'klass':klass, 'height': height}
                slide_token = Token('<video class="{klass}" src="img/{subj}/{lec}/{text}" controls muted height="{height}"></video>'.format(**d),VID)
                slides.append(slide_token)
            elif line.startswith('video:'):
                text = line[6:].strip()
                subj,lec = slide_name.split('_')

                klass = ''
                if isFragment: klass = 'fragment'
                d = {'text':text, 'subj':subj,'lec':lec,'klass':klass}
                # removed : 
                slide_token = Token('<video class="{klass}" src="img/{subj}/{lec}/{text}" controls muted width="75%" height="75%"></video>'.format(**d),VID)
                slides.append(slide_token)
            elif line.startswith('ref:'):
                text = line[4:].strip()
                token_string = '<label class="reference">[%s]</label>' % text
                slide_token = Token(token_string,HTML)
                slides.append(slide_token)
            else:
                #p
                klass = ''
                if isFragment: klass = 'fragment'
                slide_token = Token('<p class="{klass}">{text}</p>'.format(text=line,klass=klass),P)
                slides.append(slide_token)

    data['slides'] = process_slides(slides)
    data['title_top'] = data['title'].replace('<br/>','')
    
    return data

def create_presentation_file(data,slide_file):
    f = open('template.html','r')
    template = ''.join(f.readlines())
    f.close()

    contents = template.format(**data)
    f = open(slide_file,'w')
    f.write(contents)

    f.close()

def print_data(data,indent=''):
    for k,v in data.items():
        print(indent+k)
        if type(v) == dict:
            indent += '\t'
            print_data(v,indent)
        elif type(v) == list:
            for item in v:
                print(indent+'\t')
                print(item)
        else:
            print(indent+'\t')
            print(v)

def main():
    global slide_name
    slide_name = 'demo_lec1'
    # slide_name = '174_patterns'
    # slide_name = '123_lab_cover'
    # slide_name = '123_lab0'
    
    source_file,slide_file = [slide_name + '.txt',slide_name + '.html']
    source_file = 'txt/' + source_file
    data = get_slide_contents(source_file)
    create_presentation_file(data,slide_file)
    print('Successfully created {slide_name}.html'.format(slide_name=slide_name))
    #print_data(data)

if __name__ == "__main__":
    # reviewer_main()
    main()
    