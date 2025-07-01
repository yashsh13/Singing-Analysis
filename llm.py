from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv

load_dotenv()

def ai_call(parameters):
    
    response_schemas = [
        ResponseSchema(name="good", description="3 good points about the singer in a list"),
        ResponseSchema(name="mistakes", description="3 mistakes about the singer in a list"),
        ResponseSchema(name="improvements", description="3 improvement points about the singer in a list")
    ]

    parser = StructuredOutputParser.from_response_schemas(response_schemas)

    format_instructions = parser.get_format_instructions()

    prompt = PromptTemplate(
        template = "bhai main apne gaane ke ek audio file ke kuch parameters dera hu kuch feedback dede, hinglish mein bolna bhai aur ek bhi technical word use mat karna aisa like pitch vegera aur aise explain karna ki koi bhi samaj jaaye: {parameters} {format_instructions}",
        input_variables = ['parameters'],
        partial_variables = {'format_instructions':format_instructions}
    )

    model = ChatGoogleGenerativeAI(model='gemma-3-27b-it', temperature=0.7)

    chain = prompt | model | parser

    response = chain.invoke({'parameters':parameters})

    return response




