import sqlite3


def popular_banco(connection: sqlite3.Connection):
    """
    Popula o banco de dados com informações iniciais (Espécies, Pragas e Diagnóstico).
    Executa apenas se as tabelas estiverem vazias.
    """
    cursor = connection.cursor()

    # =========================================================================
    # 1. ESPÉCIES (Base de Conhecimento de Plantas)
    # =========================================================================
    cursor.execute("SELECT COUNT(*) FROM Especies")
    if cursor.fetchone()[0] == 0:
        print("🌱 Populando Espécies...")
        especies = [
            (
                "Tomate",
                "Solanum lycopersicum",
                "Regular (mantenha úmido)",
                "Sol Pleno (6h+)",
                "Remover chupões",
                "Rico em Potássio",
                "Primavera",
                "assets/especies/tomate.png",
            ),
            (
                "Hortelã",
                "Mentha sp.",
                "Diária (gosta de água)",
                "Sombra Parcial",
                "Poda de contenção",
                "Orgânico/Humus",
                "Ano todo",
                "assets/especies/hortela.png",
            ),
            (
                "Suculenta",
                "Echeveria sp.",
                "Pouca (só quando seco)",
                "Sol ou Claridade",
                "Retirar folhas secas",
                "Específico cactos",
                "Verão",
                "assets/especies/suculenta.png",
            ),
            (
                "Manjericão",
                "Ocimum basilicum",
                "Regular",
                "Sol Pleno",
                "Cortar flores",
                "Nitrogênio",
                "Verão",
                "assets/especies/manjericao.png",
            ),
            (
                "Jibóia",
                "Epipremnum aureum",
                "Moderada",
                "Sombra/Luz Indireta",
                "Limpeza de folhas",
                "NPK 10-10-10",
                "Ano todo",
                "assets/especies/jiboia.png",
            ),
        ]
        cursor.executemany(
            """
            INSERT INTO Especies (nome_popular, nome_cientifico, instrucoes_rega, necessidade_sol, necessidade_poda, uso_adubos, epoca_plantio, foto_exemplo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            especies,
        )

    # =========================================================================
    # 2. PRAGAS (Base de Conhecimento de Doenças)
    # =========================================================================
    cursor.execute("SELECT COUNT(*) FROM PragasDoencas")
    if cursor.fetchone()[0] == 0:
        print("🐛 Populando Pragas...")
        pragas = [
            (
                "Pulgão",
                "Insetos pequenos (verdes/pretos) que sugam a seiva.",
                "Folhas enroladas, amareladas e pegajosas.",
                "Óleo de Neem ou calda de sabão.",
                "assets/pragas/pulgao.png",
            ),
            (
                "Cochonilha",
                "Parece algodão branco ou escamas nos caules.",
                "Manchas brancas, planta fraca, formigas.",
                "Cotonete com álcool ou óleo mineral.",
                "assets/pragas/cochonilha.png",
            ),
            (
                "Oídio (Fungo)",
                "Pó branco sobre as folhas.",
                "Parece talco nas folhas, inibe fotossíntese.",
                "Leite cru diluído (10%) ou fungicida.",
                "assets/pragas/oidio.png",
            ),
            (
                "Lagarta",
                "Larvas que comem folhas.",
                "Buracos grandes nas folhas e fezes pretas.",
                "Remoção manual ou Bacillus thuringiensis.",
                "assets/pragas/lagarta.png",
            ),
            (
                "Falta de Água",
                "Desidratação da planta.",
                "Folhas murchas, secas e quebradiças.",
                "Regue imediatamente e verifique o solo.",
                "assets/pragas/seca.png",
            ),
        ]
        cursor.executemany(
            """
            INSERT INTO PragasDoencas (nome_comum, descricao, sintomas, tratamento, foto_exemplo)
            VALUES (?, ?, ?, ?, ?)
        """,
            pragas,
        )

    # =========================================================================
    # 3. ÁRVORE DE DIAGNÓSTICO
    # =========================================================================
    cursor.execute("SELECT COUNT(*) FROM DiagnosticoPerguntas")
    if cursor.fetchone()[0] == 0:
        print("🩺 Criando Árvore de Diagnóstico...")

        # --- PERGUNTAS ---
        ps = [
            (1, "O que você nota visualmente na planta?"),
            (2, "Esse 'branco' parece algodão ou pó?"),
            (3, "Como são esses insetos?"),
            (4, "Como estão as folhas?"),
        ]
        cursor.executemany(
            "INSERT INTO DiagnosticoPerguntas (ordem, texto_pergunta) VALUES (?, ?)", ps
        )

        # --- RESPOSTAS E FLUXO ---
        # (Texto, ID Pergunta Atual, ID Próxima Pergunta ou None se for fim)
        todas_respostas = [
            # Respostas da P1
            ("Manchas ou estruturas brancas", 1, 2),
            ("Vejo insetos caminhando/voando", 1, 3),
            ("Folhas com buracos ou murchas", 1, 4),
            # Respostas da P2
            ("Parece algodão/teia (Cochonilha)", 2, None),
            ("Parece talco/pó espalhado (Oídio)", 2, None),
            # Respostas da P3
            ("Pequenos, verdes ou pretos (Pulgão)", 3, None),
            ("Grandes/Larvas (Lagarta)", 3, None),
            # Respostas da P4
            ("Murchas e terra seca", 4, None),
            ("Com grandes buracos mordidos", 4, None),
        ]

        cursor.executemany(
            """
            INSERT INTO DiagnosticoRespostas (texto_resposta, id_pergunta, id_proxima_pergunta)
            VALUES (?, ?, ?)
        """,
            todas_respostas,
        )

        # --- MAPEAMENTO (ID Resposta -> ID Praga) ---
        # Nota: Assume-se a ordem de inserção sequencial dos IDs das respostas (1 a 9) e pragas (1 a 5)
        mapeamentos = [
            (4, 2),  # Algodão -> Cochonilha
            (5, 3),  # Pó -> Oídio
            (6, 1),  # Verdes -> Pulgão
            (7, 4),  # Larvas -> Lagarta
            (8, 5),  # Seca -> Falta de Água
            (9, 4),  # Buracos -> Lagarta
        ]

        cursor.executemany(
            "INSERT INTO DiagnosticoMapeamento (id_resposta, id_praga) VALUES (?, ?)",
            mapeamentos,
        )

    connection.commit()
