import azure.functions as func
import json
import re

app = func.FunctionApp()

def is_valid_cpf(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf)  # Remove caracteres não numéricos
    if len(cpf) != 11 or cpf in [str(i) * 11 for i in range(10)]:
        return False

    def calc_digit(digits):
        soma = sum(int(d) * i for d, i in zip(digits, range(len(digits) + 1, 1, -1)))
        return (soma * 10 % 11) % 10

    return cpf[-2:] == f"{calc_digit(cpf[:9])}{calc_digit(cpf[:10])}"

@app.function_name(name="ValidateCPF")
@app.route(route="ValidateCPF", auth_level=func.AuthLevel.ANONYMOUS)
def validate_cpf(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        cpf = req_body.get("cpf")

        if not cpf:
            return func.HttpResponse(json.dumps({"error": "CPF is required"}), status_code=400, mimetype="application/json")

        valid = is_valid_cpf(cpf)
        return func.HttpResponse(json.dumps({"cpf": cpf, "valid": valid}), status_code=200, mimetype="application/json")

    except ValueError:
        return func.HttpResponse(json.dumps({"error": "Invalid JSON"}), status_code=400, mimetype="application/json")
