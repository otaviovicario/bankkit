# data/latam/br.py
# Main Brazilian banks indexed by COMPE code
# Source: BACEN (Banco Central do Brasil) — https://www.bcb.gov.br
# NOTE: CNPJ data is static and may become outdated.
# Always verify against official BACEN sources for critical use cases.
# Last updated: 2025

BANKS = {
    "001": {"name": "Banco do Brasil",            "cnpj": "00000000000191", "swift": "BRASBRRJXXX"},
    "003": {"name": "Banco da Amazônia",           "cnpj": "04902979000144", "swift": None},
    "004": {"name": "Banco do Nordeste do Brasil", "cnpj": "07237373000120", "swift": None},
    "033": {"name": "Santander Brasil",            "cnpj": "90400888000142", "swift": "BSCHBRSPSSP"},
    "041": {"name": "Banrisul",                    "cnpj": "92702067000196", "swift": "BRGSBRRS"},
    "070": {"name": "BRB - Banco de Brasília",     "cnpj": "00000208000100", "swift": None},
    "077": {"name": "Banco Inter",                 "cnpj": "00416968000101", "swift": None},
    "104": {"name": "Caixa Econômica Federal",     "cnpj": "00360305000104", "swift": "CEFXBRSP"},
    "121": {"name": "Banco Agibank",               "cnpj": "10664513000100", "swift": None},
    "197": {"name": "Stone Pagamentos",            "cnpj": "16501555000157", "swift": None},
    "208": {"name": "BTG Pactual",                 "cnpj": "30306294000145", "swift": "BTGPBRSP"},
    "212": {"name": "Banco Original",              "cnpj": "92894922000108", "swift": None},
    "218": {"name": "Banco BS2",                   "cnpj": "71027866000134", "swift": None},
    "237": {"name": "Bradesco",                    "cnpj": "60746948000112", "swift": "BBDEBRSP"},
    "260": {"name": "Nu Pagamentos (Nubank)",       "cnpj": "18236120000158", "swift": None},
    "290": {"name": "Pagseguro (PagBank)",         "cnpj": "08561701000101", "swift": None},
    "318": {"name": "Banco BMG",                   "cnpj": "61186680000174", "swift": None},
    "336": {"name": "Banco C6",                    "cnpj": "31872495000172", "swift": None},
    "341": {"name": "Itaú Unibanco",               "cnpj": "60701190000104", "swift": "ITAUBRSP"},
    "380": {"name": "PicPay",                      "cnpj": "22896431000110", "swift": None},
    "389": {"name": "Banco Mercantil do Brasil",   "cnpj": "17184037000110", "swift": None},
    "422": {"name": "Banco Safra",                 "cnpj": "58160789000128", "swift": "SFRABRSPSAO"},
    "633": {"name": "Banco Rendimento",            "cnpj": "68900810000138", "swift": None},
    "707": {"name": "Banco Daycoval",              "cnpj": "62232889000190", "swift": None},
    "741": {"name": "Banco Ribeirão Preto",        "cnpj": "00517645000104", "swift": None},
    "745": {"name": "Citibank Brasil",             "cnpj": "33479023000180", "swift": "CITIVENXXXX"},
    "748": {"name": "Sicredi",                     "cnpj": "01181521000155", "swift": None},
    "756": {"name": "Sicoob",                      "cnpj": "02038232000164", "swift": None},
}