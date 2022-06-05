import random
import functools
from IPython.display import display, clear_output, Image
from ipywidgets import Button, Dropdown, HTML, HBox, Output
import ipywidgets as widgets
import os

# code from https://github.com/wbwvos/pidgey changed for link labelling

def annotate(examples,
             options=None,
             shuffle=False,
             include_skip=True,
             display_fn=display):
    """
    Build an interactive widget for annotating a list of input examples.

    Parameters
    ----------
    examples: list of 2-element list, list of combinations to annotate
    options: list
    shuffle: bool, shuffle the examples before annotating
    include_skip: bool, include option to skip example while annotating
    display_fn: func, function for displaying an example to the user

    Returns
    -------
    annotations : list of tuples, list of annotated examples (example[0], example[1], label)
    """
    examples = list(examples)
    
    if shuffle:
        random.shuffle(examples)
        
        
    annotations = []
    current_index = -1

    def set_label_text():
        nonlocal count_label
        count_label.value = '{} examples annotated, {} examples left'.format(
            len(annotations), len(examples) - current_index
        )

    def show_next():
        nonlocal current_index
        current_index += 1
        set_label_text()
        if current_index >= len(examples):
            for btn in buttons:
                btn.disabled = True
            print('Annotation done.')
            return
        with out:
            clear_output(wait=True)
            img1=open(examples[current_index][0],'rb').read()
            wi1 = widgets.Image(value=img1, format='jpg', width=256, height=256)
            img2=open(examples[current_index][1],'rb').read()
            wi2 = widgets.Image(value=img2, format='jpg', width=256, height=256)
            a=[wi1,wi2]
            wid=HBox(a)
            display(HBox([wi1,wi2]))

    def add_annotation(annotation):
        annotations.append((examples[current_index][0], examples[current_index][1], annotation))
        show_next()

    def skip(btn):
        show_next()

    count_label = HTML()
    set_label_text()
    display(count_label)

    if type(options) == list:
        task_type = 'classification'
    else:
        raise Exception('Invalid options')

    buttons = []
    
    if task_type == 'classification':
        use_dropdown = len(options) > 5

        if use_dropdown:
            dd = Dropdown(options=options)
            display(dd)
            btn = Button(description='submit')
            def on_click(btn):
                add_annotation(dd.value)
            btn.on_click(on_click)
            buttons.append(btn)
        
        else:
            for label in options:
                btn = Button(description=label)
                def on_click(label, btn):
                    add_annotation(label)
                btn.on_click(functools.partial(on_click, label))
                buttons.append(btn)


    else:
        print('miep')

    if include_skip:
        btn = Button(description='skip')
        btn.on_click(skip)
        buttons.append(btn)

    box = HBox(buttons)
    display(box)

    out = Output()
    display(out)

    show_next()

    return annotations

def get_combis_list(liste):
    combis = []
    for i in range(len(liste)-1):
        for j in range(i+1, len(liste)):
            combis.append([liste[i], liste[j]])
    return combis


if __name__ == '__main__':
    path = "/GitHub/GraphAesthetics-PreProcessing/investigating-aesthetics/"
    
    file_list = os.listdir(path)
    
    annotations = annotate(
      get_combis_list(file_list),
      options=['0', '1'], shuffle=True,
      display_fn=lambda filename: display(Image(filename))
    )