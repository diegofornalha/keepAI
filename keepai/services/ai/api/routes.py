from flask import Blueprint, request, jsonify
from flasgger import swag_from
from services.agent_service import AgentService

ai_blueprint = Blueprint("ai", __name__)
agent_service = AgentService()


@ai_blueprint.route("/analyze", methods=["POST"])
def analyze_text():
    """
    Analisa um texto usando IA
    ---
    tags:
      - IA
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - text
          properties:
            text:
              type: string
              description: Texto para análise
    responses:
      200:
        description: Análise concluída com sucesso
        schema:
          type: object
          properties:
            sentiment:
              type: string
              description: Sentimento do texto
            entities:
              type: array
              items:
                type: object
                properties:
                  text:
                    type: string
                  type:
                    type: string
            summary:
              type: string
              description: Resumo do texto
            topics:
              type: array
              items:
                type: string
              description: Tópicos principais
      400:
        description: Texto não fornecido
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    result = agent_service.analyze_text(data["text"])
    return jsonify(result)


@ai_blueprint.route("/generate", methods=["POST"])
def generate_content():
    """
    Gera conteúdo usando IA
    ---
    tags:
      - IA
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - prompt
          properties:
            prompt:
              type: string
              description: Prompt para geração de conteúdo
            max_tokens:
              type: integer
              description: Número máximo de tokens a gerar
              default: 100
            temperature:
              type: number
              description: Temperatura da geração (0.0 a 1.0)
              default: 0.7
    responses:
      200:
        description: Conteúdo gerado com sucesso
        schema:
          type: object
          properties:
            content:
              type: string
              description: Conteúdo gerado
            tokens_used:
              type: integer
              description: Número de tokens utilizados
      400:
        description: Prompt não fornecido
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "No prompt provided"}), 400

    result = agent_service.generate_content(data["prompt"])
    return jsonify(result)


@ai_blueprint.route("/summarize", methods=["POST"])
def summarize_text():
    """
    Resume um texto usando IA
    ---
    tags:
      - IA
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - text
          properties:
            text:
              type: string
              description: Texto para resumir
            max_length:
              type: integer
              description: Tamanho máximo do resumo em caracteres
              default: 200
    responses:
      200:
        description: Resumo gerado com sucesso
        schema:
          type: object
          properties:
            summary:
              type: string
              description: Resumo do texto
            original_length:
              type: integer
              description: Tamanho do texto original
            summary_length:
              type: integer
              description: Tamanho do resumo
      400:
        description: Texto não fornecido
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    result = agent_service.summarize_text(data["text"])
    return jsonify(result)
