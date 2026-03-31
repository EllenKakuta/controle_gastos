# 💰 Sistema de Controle Financeiro em Python

## 📌 Sobre o projeto

Este é um sistema de controle financeiro desenvolvido em Python com foco em organização de finanças pessoais.

O sistema permite registrar entradas, saídas, despesas fixas e compras no cartão de crédito, incluindo controle de parcelas e faturas.

Este projeto foi desenvolvido com o objetivo de praticar lógica de programação, organização de código e simulação de regras reais de sistemas financeiros.

---

## 🚀 Funcionalidades

* Cadastro de usuário
* Registro de salário
* Controle de saldo
* Cadastro de despesas fixas
* Registro de entradas financeiras
* Registro de saídas:
  * Débito / Pix
  * Cartão de crédito
* Controle de cartões:
  * Data de fechamento
  * Data de vencimento
* Parcelamento de compras no cartão
* Geração automática de faturas
* Correção de arredondamento de parcelas (garante soma exata)
* Extrato:
  * Geral
  * Por categoria
  * Por período
* Alerta de saldo baixo

---

## 🧠 Regras de negócio implementadas

* Compras no cartão são lançadas na fatura correta com base na data de fechamento
* Parcelas são distribuídas ao longo dos meses automaticamente
* Ajuste de centavos para evitar inconsistência no valor total
* Saldo atualizado automaticamente a cada transação
* Validação de entradas do usuário

---

## 🛠️ Tecnologias utilizadas

* Python
* Estruturas de dados (listas, dicionários)
* Manipulação de datas (`datetime`)

---

## 📂 Estrutura do projeto

Projeto desenvolvido em uma única aplicação (versão inicial - V1), com foco em lógica e regras de negócio.

Evoluções futuras incluem:
* Refatoração para Programação Orientada a Objetos (POO)
* Separação em módulos
* Interface gráfica ou API

---

## 📈 Evolução do projeto

Este projeto faz parte de uma evolução contínua de aprendizado.

Próximas versões planejadas:
* V2: Refatoração para POO
* V3: Melhor organização de camadas
* V4: Possível integração com banco de dados

---

## 🎯 Objetivo

Desenvolver habilidades práticas em:
* Lógica de programação
* Modelagem de regras de negócio
* Estruturação de sistemas
* Boas práticas de desenvolvimento

---

## 💡 Observações

Este projeto foi desenvolvido com foco em aprendizado e evolução contínua. Melhorias e refatorações fazem parte do processo.

---

## 👩‍💻 Autora

Projeto desenvolvido por mim durante minha contínua jornada de estudos em Python 
