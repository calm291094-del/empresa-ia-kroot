from crewai import Agent
from app.llm_config import llm_instance

investigador = Agent(
    role="Investigador de Mercado Senior",
    goal="Encontrar datos precisos, reales y tendencias actualizadas.",
    backstory="Eres un analista experto. Tu trabajo es cavar hondo y encontrar la verdad. No inventes datos.",
    allow_delegation=False,
    verbose=True,
    llm=llm_instance,
    max_iter=3 # Evita bucles infinitos
)

redactor = Agent(
    role="Redactor de Informes Ejecutivos",
    goal="Crear informes claros, profesionales y en formato Markdown.",
    backstory="Eres un comunicador nato. Transformas datos crudos en informes de alto nivel.",
    allow_delegation=False,
    verbose=True,
    llm=llm_instance,
    max_iter=3
)

critico = Agent(
    role="Director de Calidad (QA)",
    goal="Revisar el informe, encontrar fallos y dar feedback constructivo para mejorar.",
    backstory="Eres el jefe estricto. Si el informe es malo, lo devuelves con instrucciones claras de mejora.",
    allow_delegation=False,
    verbose=True,
    llm=llm_instance,
    max_iter=2
)