from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
from sanic import Sanic
from sanic.response import json

app = Sanic.get_app("Rasa")

@app.route("/stop", methods=["GET"])
async def stop_server(request):
    app.stop()
    return json({"message": "Server stopping..."})

class ActionHandleUnknown(Action):
    def name(self) -> Text:
        return "action_handle_unknown"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Lưu câu hỏi chưa hiểu
        current_phrase = tracker.latest_message.get('text')
        unknown_phrases = tracker.get_slot("unknown_phrases") or []

        if current_phrase not in unknown_phrases:
            unknown_phrases.append(current_phrase)

        return [SlotSet("unknown_phrases", unknown_phrases)]


class ActionHandleBullying(Action):
    def name(self) -> Text:
        return "action_handle_bullying"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        person = next(tracker.get_latest_entity_values("person"), None)

        if person:
            response = f"Bạn {person} thật là hư! Tớ sẽ chỉ bé cách xử lý nhé:\n"
            response += "1. Bình tĩnh nói 'Dừng lại!'\n"
            response += "2. Kể ngay với cô giáo\n"
            response += "3. Nhờ bạn khác giúp đỡ"
        else:
            response = "Ai bắt nạt bé vậy? Bé nhớ:\n"
            response += "1. Không khóc lóc một mình\n"
            response += "2. Kể với người lớn ngay\n"
            response += "3. Ghi lại sự việc"

        dispatcher.utter_message(text=response)
        return []

class ActionLearnNewPhrase(Action):
    def name(self) -> Text:
        return "action_learn_new_phrase"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Nhận phản hồi từ người dùng
        user_response = tracker.latest_message.get('text')
        last_unknown = tracker.get_slot("unknown_phrases")[-1] if tracker.get_slot("unknown_phrases") else None

        if last_unknown:
            learned_data = tracker.get_slot("learned_responses") or {}
            learned_data[last_unknown] = user_response

            # Lưu vào file (có thể thay bằng database)
            with open('learned_phrases.json', 'w', encoding='utf-8') as f:
                json.dump(learned_data, f, ensure_ascii=False)

            dispatcher.utter_message(text="Tớ đã học được rồi! Cảm ơn bé đã dạy tớ ❤️")
            return [SlotSet("learned_responses", learned_data)]

        return []