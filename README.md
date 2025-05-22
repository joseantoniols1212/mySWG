# mySWG – Static Website Generator

mySWG is a lightweight static site generator written in Python. It
transforms content written in Markdown into a fully navigable static website, ready for deployment.

## 🚀 Features

- 📄 Automatic conversion from Markdown to HTML
- 🧱 Template-based HTML layout system
- 🗂️ Directory-based content organization

## ▶️ How to Use

1. You write all your content in Markdown in the content directory. You can have multiple pages,
for that follow the next structure:
```
content
├── blog
│   ├── glorfindel
│   │   └── index.md
│   ├── majesty
│   │   └── index.md
│   └── tom
│       └── index.md
├── contact
│   └── index.md
└── index.md
```
Any file not related to Markdown (e.g., CSS files or images) should be placed in the static folder.

2. Then, in the script `build.sh`, you must set the basepath where your website will be
deployed (usually /, but for GitHub Pages it should be the name of your repository).

3. Finally, execute `build.sh` and your HTML files will be generated into the `docs/` folder.

## 🛠️ Requirements
- Python 3.7 or newer (nothing fancy — just not ancient)