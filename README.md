# 🌍 Earth-Blender

**Projeto de Chimpi-hackintosh** para criar uma Terra 3D estilizada no **Blender** usando Python e a API `bpy`

> Os continentes e oceanos são gerados de forma **procedural e artística**: não representam um mapa geográfico preciso

## ✨ Recursos

- 🌎 Planeta 3D com oceanos, áreas verdes, montanhas e gelo estilizados
- ☁️ Camada de nuvens procedurais
- 💡 Iluminação, câmera e fundo espacial
- 💾 Salva um arquivo `.blend` editável
- 🖼️ Renderiza um PNG opcional
- 📴 Funciona offline, sem baixar texturas
- 🖥️ Compatível com Windows, Linux e macOS que executem Blender 3.6+

## 🚀 Como usar

1. Instale o Blender a partir do site oficial: https://www.blender.org/download/
2. Baixe o arquivo `earth_blender.py` deste repositório
3. Abra o Blender, vá para **Scripting**, abra o script e clique em **Run Script**
4. A cena será criada e o arquivo `earth_scene.blend` será salvo na pasta de trabalho atual

### Pelo terminal

```bash
blender --background --python earth_blender.py
```

Para criar a cena **e** gerar uma imagem:

```bash
blender --background --python earth_blender.py -- --render
```

Para definir resolução e nome do projeto:

```bash
blender --background --python earth_blender.py -- --resolution 1080 --output meu_planeta.blend --render
```

Os arquivos de saída, por padrão, são `earth_scene.blend` e `earth_render.png`

## 📁 Estrutura

```text
Earth-Blender/
├── earth_blender.py    # Gerador do planeta
├── README.md           # Documentação
├── LICENSE             # Licença MIT
└── .gitignore
```

## 🛠️ Personalização

Edite os valores em `earth_blender.py` para alterar cores, ruído do terreno, iluminação, câmera e nuvens

## 👤 Autor

**Chimpi-hackintosh**

Projeto original deste repositório sob licença MIT; veja [LICENSE](LICENSE)

**Observação:** o resultado visual não foi testado automaticamente no Blender neste commit
