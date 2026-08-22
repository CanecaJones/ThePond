# Decisões do projeto — The Pond

## Stack
- Backend: Django + DRF
- Frontend: Vue (Vite)
- Auth: JWT, sem e-mail, sem recuperação de senha (usuário é responsável por guardar a senha)

## Modelo de usuário
- username, @handle (editável), senha — sem campo de e-mail, sem código mestre de recuperação

## Posts
- Limite de 300 caracteres
- Suporte a mídia desde o MVP: imagem, vídeo (até 20MB), áudio, links

## Fases
- MVP: auth, posts com mídia, follow, like, repost, feed cronológico
- Fase 2+: notificações, posts fixados de admin, promoted posts, sistema de mods, algoritmo de feed próprio, integração com Groq

## Histórico de mudanças
- Frontend trocado de React para Vue (mais leve, curva de aprendizado menor)