from .workflow import app

class LLMApp:
    def __init__(self):
        self.__llm_app = app
        self.__result = None

    def invoke(self, input: dict = None, **kwargs):
        user_input = input or kwargs
        if not user_input:
            raise ValueError("input is required")
        try:
            self.__result = self.__llm_app.invoke(user_input)
        except Exception as err:
            raise err
        return self.__result
    
    async def ainvoke(self, input: dict = None, **kwargs):
        user_input = input or kwargs
        if not user_input:
            raise ValueError("input is required")
        try:
            self.__result = await self.__llm_app.ainvoke(user_input)
        except Exception as err:
            raise err
        return self.__result
    
    @property
    def result(self):
        return self.__result