from components.button import Button


class ButtonService():

    async def button(self, custom_button):
        buttons, payload, url = [], None, None 
        for button in custom_button:
            if button.get("payload"): 
                type = "postback" 
                payload, url = button.get("payload"), None 
            else: 
                type ="web_url"  
                url,payload = button.get("url"), None 
            buttons.append(Button(type=type, 
                                  title=button.get("title"),
                                  payload=payload, 
                                  url=url
                                ).dict()) 
        return buttons
