import json
import urllib3
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler

http = urllib3.PoolManager()

class ConsultarTareasIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (
            ask_utils.is_intent_name("ConsultarTareasIntent")(handler_input) or
            ask_utils.is_request_type("LaunchRequest")(handler_input)
        )

    def handle(self, handler_input):
        url = "url/grok"
        headers = {"ngrok-skip-browser-warning": "true"}
        
        try:
            response = http.request('GET', url, headers=headers)
            if response.status == 200:
                data = json.loads(response.data.decode('utf-8'))
                tareas = data.get("tareas", [])
                
                if not tareas:
                    speech_text = "No tienes ninguna tarea registrada en tu base de datos."
                else:
                    speech_text = "Tus tareas registradas son: "
                    for t in tareas:
                        speech_text += f"En {t['materia']}, {t['descripcion']}. "
            else:
                speech_text = "El servidor respondió con un error."
        except Exception as e:
            speech_text = "No me pude conectar al servidor local. Revisa Flask y Ngrok."

        return handler_input.response_builder.speak(speech_text).response

class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speech_text = "Puedes pedirme la lista de tareas."
        return handler_input.response_builder.speak(speech_text).ask(speech_text).response

class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or 
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        return handler_input.response_builder.speak("¡Hasta luego!").response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        return handler_input.response_builder.response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        speech_text = "Ocurrió un error al procesar tu solicitud."
        return handler_input.response_builder.speak(speech_text).response

# Registro de Handlers
sb = CustomSkillBuilder()
sb.add_request_handler(ConsultarTareasIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
