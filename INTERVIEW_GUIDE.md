# Guia de entrevista — document-data-extractor

## Problema, arquitetura e decisões

O problema é transformar documentos textuais de um layout conhecido em registros verificáveis. A CLI chama extraction → transformation → validation → export. Regex reconhece rótulos; Decimal mantém valores precisos; Pandas produz CSV. Não há banco ou endpoints: a interface é CLI e a persistência são os arquivos de saída. Registros inconsistentes são mantidos com motivos, e falhas de leitura não interrompem o lote. Os testes incluem arquivos de amostra e destinos temporários. Estude `extractor/cli.py`, `validation.py` e `tests/test_extractor.py`. Em produção, priorize escrita atômica, layouts versionados e streaming; OCR/PDF não estão implementados.

## Roteiro de estudo

1. Execute os comandos do [README](README.md) e observe as saídas.
2. Execute os testes e leia os casos antes de alterar as regras.
3. Acompanhe uma entrada desde o contrato até a persistência ou saída.
4. Reproduza uma falha de validação e explique sua resposta.
5. Distinga o que foi implementado, o que foi validado e o que é melhoria futura.

## 15 perguntas com respostas

### 1. Por que regex é adequada aqui?

O layout textual é conhecido e pequeno. Regex identifica rótulos explícitos, sem exigir interpretação semântica. Ela não resolve documentos arbitrários, scans ou PDFs.

### 2. Como campos repetidos são tratados?

`extract` conta ocorrências. Quantidade diferente de um registra inconsistência. A primeira ocorrência é preservada para inspeção, mas o registro é marcado inválido.

### 3. Como valores monetários são normalizados?

Vírgula indica separador decimal e pontos são removidos como milhares; sem vírgula, ponto é decimal. Decimal evita arredondamento binário; JSON guarda o valor em texto.

### 4. Por que não usar float?

Float pode representar valores decimais com pequenas diferenças. Decimal preserva a representação necessária para validar centavos. A exportação não realiza cálculos financeiros.

### 5. Quais validações existem?

ID no padrão DEMO-0000, prefixo FICTITIOUS, data ISO válida, valor positivo finito e no máximo duas casas decimais. Também se detecta duplicidade entre arquivos do lote.

### 6. Como a duplicidade é determinada?

Arquivos são ordenados por nome; um conjunto guarda IDs vistos. A segunda ocorrência recebe erro. A escolha é determinística, mas não deduplica ou mescla dados.

### 7. O que acontece com um registro inválido?

Ele continua no JSON e CSV com `valid=false` e motivos. Isso torna falhas inspecionáveis, em vez de descartá-las silenciosamente.

### 8. Qual é o papel do Pandas?

Constrói o DataFrame com colunas previsíveis, serializa erros para CSV e exporta. Extração e regras permanecem funções Python pequenas e independentes.

### 9. Como o CSV evita execução de fórmulas?

Strings iniciadas por =, +, - ou @, após espaços, recebem apóstrofo. A transformação só afeta CSV; JSON preserva o valor original para auditoria.

### 10. Como arquivos ilegíveis são tratados?

OSError e UnicodeError geram um registro inválido com nome do arquivo e tipo de falha. O lote continua. Erros ao escrever o destino continuam sendo falhas da execução.

### 11. Por que não há banco?

O objetivo é processamento local de um lote e exportação. Arquivos são suficientes para a demonstração. Um banco seria útil se fossem exigidos histórico, pesquisa ou reprocessamento persistentes.

### 12. Como é testado o pipeline?

Os testes processam samples em destino temporário, conferem contagens e leem JSON e CSV novamente. Testes unitários verificam normalização, validação e campos repetidos.

### 13. O que ocorre com um lote vazio?

O relatório retorna zero e o CSV contém cabeçalhos sem registros. Isso permite leitura posterior sem erro de ausência de colunas.

### 14. Quais são as limitações de memória?

Todos os registros são acumulados e o DataFrame é criado ao final. Para lotes extensos, processamento por chunks e saída incremental reduziriam o consumo.

### 15. Como adaptar para documentos reais?

Definiria layouts versionados e políticas de validação por origem autorizada, removeria o prefixo de demonstração e acrescentaria testes com dados anonimizados. OCR e PDF exigem módulos novos.

