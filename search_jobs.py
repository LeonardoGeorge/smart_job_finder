"""
🚀 SMART JOB FINDER - SEU ASSISTENTE DE CARREIRA INTELIGENTE
Desenvolvido por: Leonardo George
GitHub: github.com/LeonardoGeorge
"""

import json
import random
from datetime import datetime, timedelta
import re


class SmartJobFinder:
    def __init__(self):
        self.vagas = self.carregar_vagas_exemplo()
        self.usuario = {}
        self.candidaturas = []

    def carregar_vagas_exemplo(self):
        """Base de dados de vagas exemplo - no mundo real viria de uma API"""
        return [
            {
                "id": 1,
                "titulo": "Desenvolvedor Python Júnior",
                "empresa": "TechSolutions BR",
                "salario": "R$ 3.500 - R$ 4.500",
                "localidade": "Remoto",
                "tipo": "CLT",
                "skills": ["Python", "Django", "Git", "SQL"],
                "descricao": "Vaga para iniciantes em desenvolvimento Backend",
                "data_publicacao": (datetime.now() - timedelta(days=2)).strftime("%d/%m/%Y"),
                "nivel": "Júnior"
            },
            {
                "id": 2,
                "titulo": "Analista de Dados Pleno",
                "empresa": "DataInsights Corp",
                "salario": "R$ 6.000 - R$ 8.000",
                "localidade": "São Paulo - SP",
                "tipo": "PJ",
                "skills": ["Python", "Pandas", "SQL", "Power BI", "Excel"],
                "descricao": "Análise de dados e criação de relatórios estratégicos",
                "data_publicacao": (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y"),
                "nivel": "Pleno"
            },
            {
                "id": 3,
                "titulo": "Desenvolvedor Full Stack",
                "empresa": "StartupInovadora",
                "salario": "R$ 7.000 - R$ 9.000",
                "localidade": "Híbrido - Rio de Janeiro",
                "tipo": "CLT",
                "skills": ["Python", "JavaScript", "React", "Node.js", "MongoDB"],
                "descricao": "Desenvolvimento de aplicações web completas",
                "data_publicacao": datetime.now().strftime("%d/%m/%Y"),
                "nivel": "Pleno"
            },
            {
                "id": 4,
                "titulo": "Cientista de Dados Sênior",
                "empresa": "BigData Analytics",
                "salario": "R$ 12.000 - R$ 15.000",
                "localidade": "Remoto",
                "tipo": "PJ",
                "skills": ["Python", "Machine Learning", "TensorFlow", "SQL", "Estatística"],
                "descricao": "Desenvolvimento de modelos preditivos e IA",
                "data_publicacao": (datetime.now() - timedelta(days=3)).strftime("%d/%m/%Y"),
                "nivel": "Sênior"
            }
        ]

    def cadastrar_usuario(self):
        """Cadastro do perfil profissional"""
        print("\n" + "=" * 50)
        print("👤 CADASTRO DO SEU PERFIL PROFISSIONAL")
        print("=" * 50)

        self.usuario["nome"] = input("📝 Seu nome completo: ")
        self.usuario["email"] = input("📧 Seu e-mail: ")
        self.usuario["nivel"] = input("🎯 Nível profissional (Júnior/Pleno/Sênior): ").capitalize()

        print("\n💻 Digite suas habilidades (separadas por vírgula):")
        skills_input = input("Ex: Python, SQL, JavaScript, Git: ")
        self.usuario["skills"] = [skill.strip() for skill in skills_input.split(",")]

        print("\n🎉 Perfil cadastrado com sucesso!")

    def calcular_compatibilidade(self, vaga):
        """Calcula a compatibilidade entre usuário e vaga"""
        if not self.usuario:
            return 0

        skills_usuario = set([s.lower() for s in self.usuario.get("skills", [])])
        skills_vaga = set([s.lower() for s in vaga["skills"]])

        # Compatibilidade por skills
        skills_comuns = skills_usuario.intersection(skills_vaga)
        percentual_skills = len(skills_comuns) / len(skills_vaga) * 70  # 70% do score

        # Compatibilidade por nível (30% do score)
        nivel_usuario = self.usuario.get("nivel", "").lower()
        nivel_vaga = vaga["nivel"].lower()

        niveis = {"júnior": 1, "pleno": 2, "sênior": 3}
        nivel_score = 0

        if nivel_usuario in niveis and nivel_vaga in niveis:
            diff = abs(niveis[nivel_usuario] - niveis[nivel_vaga])
            nivel_score = max(0, 30 - (diff * 15))  # Penaliza diferença de nível

        return min(100, percentual_skills + nivel_score)

    def buscar_vagas(self):
        """Sistema inteligente de busca de vagas"""
        if not self.usuario:
            print("❌ Cadastre seu perfil primeiro!")
            return

        print("\n" + "=" * 50)
        print("🔍 SISTEMA INTELIGENTE DE BUSCA")
        print("=" * 50)

        # Filtros
        print("\n🎯 Escolha filtros de busca:")
        print("1. 🔍 Buscar por palavra-chave")
        print("2. 🏢 Buscar por empresa")
        print("3. 📍 Buscar por localidade")
        print("4. 🎖️ Buscar por nível")
        print("5. 🔄 Ver todas as vagas")

        opcao = input("\n👉 Sua opção: ")

        vagas_filtradas = self.vagas.copy()

        if opcao == "1":
            termo = input("🔎 Digite a palavra-chave: ").lower()
            vagas_filtradas = [v for v in vagas_filtradas if
                               termo in v["titulo"].lower() or termo in v["descricao"].lower()]
        elif opcao == "2":
            empresa = input("🏢 Digite o nome da empresa: ").lower()
            vagas_filtradas = [v for v in vagas_filtradas if empresa in v["empresa"].lower()]
        elif opcao == "3":
            local = input("📍 Digite a localidade: ").lower()
            vagas_filtradas = [v for v in vagas_filtradas if local in v["localidade"].lower()]
        elif opcao == "4":
            nivel = input("🎖️ Digite o nível (Júnior/Pleno/Sênior): ").capitalize()
            vagas_filtradas = [v for v in vagas_filtradas if nivel == v["nivel"]]

        # Ordenar por compatibilidade
        vagas_com_score = []
        for vaga in vagas_filtradas:
            score = self.calcular_compatibilidade(vaga)
            vagas_com_score.append((vaga, score))

        vagas_com_score.sort(key=lambda x: x[1], reverse=True)

        # Exibir resultados
        print(f"\n🎯 ENCONTRAMOS {len(vagas_com_score)} VAGA(S) PARA VOCÊ:")

        for vaga, score in vagas_com_score:
            self.exibir_vaga(vaga, score)

    def exibir_vaga(self, vaga, score=None):
        """Exibe uma vaga de forma organizada"""
        print(f"\n{'=' * 60}")
        print(f"🏢 {vaga['empresa']}")
        print(f"📋 {vaga['titulo']}")
        print(f"💰 {vaga['salario']} | 📍 {vaga['localidade']}")
        print(f"📄 {vaga['tipo']} | 🎖️ {vaga['nivel']}")
        print(f"📅 Publicada em: {vaga['data_publicacao']}")

        if score is not None:
            emoji_score = "🔴" if score < 40 else "🟡" if score < 70 else "🟢"
            print(f"✅ {emoji_score} Compatibilidade: {score:.1f}%")

        print(f"🛠️  Skills: {', '.join(vaga['skills'])}")
        print(f"📝 {vaga['descricao']}")
        print(f"{'=' * 60}")

    def candidatar_vaga(self):
        """Sistema de candidatura a vagas"""
        if not self.usuario:
            print("❌ Cadastre seu perfil primeiro!")
            return

        print("\n🎯 VAGAS DISPONÍVEIS PARA CANDIDATURA:")
        for i, vaga in enumerate(self.vagas, 1):
            print(f"{i}. {vaga['titulo']} - {vaga['empresa']}")

        try:
            escolha = int(input("\n👉 Número da vaga para candidatar: ")) - 1
            if 0 <= escolha < len(self.vagas):
                vaga = self.vagas[escolha]
                score = self.calcular_compatibilidade(vaga)

                print(f"\n🎊 CANDIDATURA REALIZADA!")
                print(f"📋 Vaga: {vaga['titulo']}")
                print(f"🏢 Empresa: {vaga['empresa']}")
                print(f"✅ Sua compatibilidade: {score:.1f}%")

                # Salvar candidatura
                candidatura = {
                    "vaga": vaga["titulo"],
                    "empresa": vaga["empresa"],
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "compatibilidade": score
                }
                self.candidaturas.append(candidatura)

                # Dicas personalizadas
                if score < 50:
                    print("\n💡 DICA: Considere melhorar suas skills para aumentar suas chances!")
                else:
                    print("\n🎉 Boa sorte! Suas chances são excelentes!")

            else:
                print("❌ Número de vaga inválido!")
        except ValueError:
            print("❌ Digite um número válido!")

    def minhas_candidaturas(self):
        """Histórico de candidaturas"""
        if not self.candidaturas:
            print("\n📭 Você ainda não se candidatou a nenhuma vaga.")
            return

        print("\n" + "=" * 50)
        print("📋 HISTÓRICO DE CANDIDATURAS")
        print("=" * 50)

        for i, cand in enumerate(self.candidaturas, 1):
            print(f"\n{i}. {cand['vaga']}")
            print(f"   🏢 {cand['empresa']}")
            print(f"   📅 {cand['data']}")
            print(f"   ✅ Compatibilidade: {cand['compatibilidade']:.1f}%")

    def estatisticas_mercado(self):
        """Estatísticas do mercado de trabalho"""
        print("\n" + "=" * 50)
        print("📊 ESTATÍSTICAS DO MERCADO")
        print("=" * 50)

        # Estatísticas básicas
        total_vagas = len(self.vagas)
        niveis = {}
        skills_count = {}

        for vaga in self.vagas:
            # Contar níveis
            niveis[vaga["nivel"]] = niveis.get(vaga["nivel"], 0) + 1

            # Contar skills
            for skill in vaga["skills"]:
                skills_count[skill] = skills_count.get(skill, 0) + 1

        print(f"\n📈 TOTAL DE VAGAS: {total_vagas}")
        print("\n🎖️ DISTRIBUIÇÃO POR NÍVEL:")
        for nivel, count in niveis.items():
            percentual = (count / total_vagas) * 100
            print(f"   {nivel}: {count} vaga(s) ({percentual:.1f}%)")

        print("\n🛠️ SKILLS MAIS PROCURADAS:")
        skills_ordenadas = sorted(skills_count.items(), key=lambda x: x[1], reverse=True)
        for skill, count in skills_ordenadas[:5]:  # Top 5
            percentual = (count / total_vagas) * 100
            print(f"   {skill}: {count} ocorrências ({percentual:.1f}%)")

        if self.usuario:
            print(f"\n💼 SEU PERFIL: {self.usuario['nivel']}")
            print(f"🛠️  SUAS SKILLS: {', '.join(self.usuario['skills'])}")


def main():
    sistema = SmartJobFinder()

    while True:
        print("\n" + "=" * 60)
        print("🚀 SMART JOB FINDER - SEU ASSISTENTE DE CARREIRA")
        print("=" * 60)
        print("1. 👤 Cadastrar Meu Perfil")
        print("2. 🔍 Buscar Vagas Inteligente")
        print("3. 📄 Ver Todas as Vagas")
        print("4. 🎯 Candidatar a Vaga")
        print("5. 📋 Minhas Candidaturas")
        print("6. 📊 Estatísticas do Mercado")
        print("7. 🚪 Sair")

        opcao = input("\n👉 Escolha uma opção (1-7): ")

        if opcao == "1":
            sistema.cadastrar_usuario()
        elif opcao == "2":
            sistema.buscar_vagas()
        elif opcao == "3":
            print("\n📄 TODAS AS VAGAS DISPONÍVEIS:")
            for vaga in sistema.vagas:
                sistema.exibir_vaga(vaga)
        elif opcao == "4":
            sistema.candidatar_vaga()
        elif opcao == "5":
            sistema.minhas_candidaturas()
        elif opcao == "6":
            sistema.estatisticas_mercado()
        elif opcao == "7":
            print("\n👋 Obrigado por usar o Smart Job Finder!")
            print("🎉 Boa sorte na sua busca por emprego!")
            break
        else:
            print("❌ Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()