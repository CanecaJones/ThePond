# The Pond

Rede social minimalista e independente, inspirada no formato do Twitter/X — feita do zero com Django (backend) e Vue (frontend).

## Sobre o projeto

The Pond é uma plataforma social onde qualquer pessoa pode criar uma conta, seguir outras pessoas, publicar posts com texto, imagem, vídeo (até 20MB) e áudio (estilo WhatsApp), curtir, repostar e comentar.

O projeto é construído em fases (MVP → expansão), com foco em simplicidade no início e evolução incremental de funcionalidades como:
- Sistema de notificações
- Posts fixados/broadcast do administrador
- Posts promovidos
- Sistema de moderação (mods)
- Algoritmo de feed próprio
- Geração automática de posts via API da Groq

## Stack

- **Backend:** Django + Django REST Framework
- **Frontend:** Vue (Vite)
- **Banco de dados:** PostgreSQL (a definir/confirmar)
- **Autenticação:** JWT (usuário + senha, sem e-mail, sem recuperação)

## Status

Em desenvolvimento — fase MVP.

## 📄 Documentação

Veja a pasta [`/docs`](./docs) para detalhes de arquitetura, modelos de dados e decisões de projeto.