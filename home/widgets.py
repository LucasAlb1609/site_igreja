# seu_app/widgets.py

import os
from django import forms
from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe

def get_icon_choices():
    """
    Escaneia o diretório de ícones e retorna uma lista de tuplas
    (nome_do_arquivo_sem_extensao, nome_do_arquivo_sem_extensao)
    para ser usada como 'choices' em um formulário.
    """
    icon_dir_path = os.path.join(settings.BASE_DIR, 'static', 'fotos', 'ícones', 'agenda')
    choices = []

    if not os.path.exists(icon_dir_path):
        print(f"AVISO: O diretório de ícones não foi encontrado em '{icon_dir_path}'")
        return [('', 'Nenhum ícone encontrado')]

    for filename in sorted(os.listdir(icon_dir_path)):
        if filename.lower().endswith(('.png', '.svg', '.jpg', '.jpeg', '.gif')):
            name_without_extension = os.path.splitext(filename)[0]
            choices.append((name_without_extension, name_without_extension))
            
    return choices

class IconSelectorWidget(forms.RadioSelect):
    """
    Um widget que renderiza opções de rádio com uma imagem e o nome do ícone.
    Esta versão foi corrigida para garantir a interatividade do clique.
    """
    def render(self, name, value, attrs=None, renderer=None):
        """Renderiza o widget como uma lista de ícones clicáveis."""
        
        # Inicia a construção do nosso layout visual
        final_html = '<div style="display: flex; flex-wrap: wrap; gap: 15px; margin-top: 10px;">'
        
        for i, choice in enumerate(self.choices):
            choice_value = choice[0]
            
            # Localiza a URL estática do ícone
            static_url = None
            icon_path_rel = os.path.join('fotos', 'ícones', 'agenda')
            icon_dir_abs = os.path.join(settings.BASE_DIR, 'static', icon_path_rel)

            if os.path.exists(icon_dir_abs):
                for filename in os.listdir(icon_dir_abs):
                    if os.path.splitext(filename)[0] == choice_value:
                        static_url = os.path.join(settings.STATIC_URL, icon_path_rel, filename)
                        break

            if static_url:
                is_checked = str(choice_value) == str(value)
                radio_id = f'id_{name}_{i}'
                
                # *** CORREÇÃO PRINCIPAL AQUI ***
                # Usamos <label> como o container principal para garantir o clique nativo.
                # O input radio é visualmente escondido, mas funcional.
                final_html += format_html(
                    """
                    <label class="icon-selector-label {selected_class}" data-group="{name}">
                        <input type="radio" name="{name}" value="{value}" id="{radio_id}" style="opacity:0; width:0; height:0; position:absolute;" {checked}>
                        <div class="icon-selector-content">
                            <img src="{icon_url}" alt="{alt_text}">
                            <span>{label_text}</span>
                        </div>
                    </label>
                    """,
                    selected_class='selected' if is_checked else '',
                    name=name,
                    value=choice_value,
                    radio_id=radio_id,
                    checked='checked' if is_checked else '',
                    icon_url=static_url,
                    alt_text=choice[1],
                    label_text=choice[1]
                )

        final_html += '</div>'
        
        # Adiciona CSS e JavaScript para o feedback visual dinâmico
        script_and_style = format_html(
            """
            <style>
                .icon-selector-label {{
                    text-align: center;
                    border: 2px solid #ccc;
                    padding: 10px;
                    border-radius: 8px;
                    cursor: pointer;
                    transition: border-color 0.2s ease-in-out;
                }}
                .icon-selector-label.selected {{
                    border-color: #007bff; /* Cor quando selecionado */
                }}
                .icon-selector-label:hover {{
                    border-color: #888;
                }}
                .icon-selector-content img {{
                    width: 48px;
                    height: 48px;
                    display: block;
                    margin-bottom: 5px;
                }}
                .icon-selector-content span {{
                    font-family: sans-serif;
                    font-size: 12px;
                }}
            </style>
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    const radios = document.querySelectorAll('input[type="radio"][name="{name}"]');
                    radios.forEach(radio => {{
                        radio.addEventListener('change', function() {{
                            // Remove a classe 'selected' de todas as labels do mesmo grupo
                            document.querySelectorAll('.icon-selector-label[data-group="{name}"]').forEach(label => {{
                                label.classList.remove('selected');
                            }});
                            // Adiciona a classe 'selected' na label pai do radio checado
                            if (this.checked) {{
                                this.parentElement.classList.add('selected');
                            }}
                        }});
                    }});
                }});
            </script>
            """, name=name
        )

        return mark_safe(final_html + script_and_style)