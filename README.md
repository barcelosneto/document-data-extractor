# Document Data Extractor

Pipeline local de extração, normalização, validação e exportação de documentos textuais com um layout conhecido. Os exemplos incluídos permitem reproduzir um processamento com documentos válidos e inconsistentes.

## Tecnologias

Python, expressões regulares, Decimal, Pandas, JSON, CSV e Pytest.

## Funcionalidades

Leitura de arquivos `.txt` UTF-8; identificação de quatro campos; detecção de campos ausentes ou repetidos; normalização de espaços, identificadores e valores; validação de datas, valores positivos e duplicidade de IDs; exportação de todos os registros e relatório agregado. CSV protege células iniciadas por caracteres de fórmula.

## Instalação

Requisitos: Python 3.11 ou superior e acesso à internet para instalar as dependências. Execute na raiz deste repositório. Os comandos abaixo usam PowerShell e não exigem ativar o ambiente virtual.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Em Linux/macOS, use `python3` na criação do ambiente e `.venv/bin/python` no lugar de `.\.venv\Scripts\python.exe`.

## Execução

```powershell
.\.venv\Scripts\python.exe -m extractor.cli --input samples --output output
```

O comando produz `output/records.csv`, `output/records.json` e `output/report.json`. A pasta de saída fica fora do controle de versão. Arquivos existentes com esses nomes são substituídos em execuções posteriores.

## Exemplo de documento

```text
FICTIONAL DOCUMENT — all information is invented.
Document-ID: DEMO-0001
Company: FICTITIOUS Example Workshop
Issue-Date: 2025-01-10
Amount: 1.250,50
```

O valor vira `"1250.50"`, preservando precisão decimal como texto no JSON. Números com vírgula usam a convenção decimal brasileira; sem vírgula, ponto é separador decimal. Não há inferência automática de locale.

Resumo esperado para os três documentos incluídos:

```json
{"total":3,"valid":1,"invalid":2,"error_count":3}
```

Exemplo de registro válido:

```json
{"document_id":"DEMO-0001","company":"FICTITIOUS Example Workshop","issue_date":"2025-01-10","amount":"1250.50","source":"01-valid.txt","valid":true,"errors":[]}
```

O segundo documento tem data e valor inválidos; o terceiro repete um ID. Registros inválidos permanecem na saída com `valid=false` e motivos em `errors`; nenhum descarte silencioso acontece. A ordenação por nome de arquivo torna a primeira ocorrência de um ID a referência. Todos os nomes, datas e valores são inventados.

## Arquitetura

`extraction.py` reconhece campos por regex; `transformation.py` normaliza; `validation.py` verifica regras; `export.py` usa Pandas para CSV; `cli.py` coordena o pipeline. `samples/` contém as entradas e `tests/` as verificações.

Não há banco de dados ou endpoints HTTP. Os arquivos JSON e CSV são o resultado persistente. Pasta inexistente gera erro de CLI; arquivo ilegível gera um registro inválido identificado pelo nome do arquivo.

## Testes

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Os testes são locais e não exigem credenciais nem serviços externos.

A suíte cobre normalização, campos ausentes/repetidos, valores não finitos, duplicidade, execução completa, diretório vazio e proteção de CSV.

## Limitações e melhorias futuras

Suporta texto estruturado no layout demonstrado; não implementa PDF, OCR ou interpretação de documentos arbitrários. O prefixo `FICTITIOUS` é obrigatório para empresas nesta demonstração. Para produção, separar políticas de demonstração, criar layouts versionados e escrita atômica de saídas, processar lotes com streaming e integrar formatos reais autorizados.

## Documentação adicional

- [Guia de entrevista](INTERVIEW_GUIDE.md)
- [Comandos de publicação](GIT_SETUP.md)
- [Licença MIT](LICENSE)

Todos os dados de demonstração são fictícios. As aplicações foram projetadas para demonstração local; não possuem autenticação de usuários.
