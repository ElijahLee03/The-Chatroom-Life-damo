import os
import json
import time

def add_post_to_json(jsonPath, writer, new_title, new_content):
    try:
        # 기존 JSON 파일 읽어오기
        with open(jsonPath, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # 파일이 없거나 JSON 디코딩에 실패할 경우, 빈 리스트로 초기화
        data = []

    # 새로운 데이터 추가
    new_post = {
        "writer": writer,
        "time": time.strftime('%Y-%m-%d_%H_%M_%S'),
        "title": new_title,
        "content": new_content
    }
    data.append(new_post)

    # 수정된 데이터를 다시 JSON 파일에 저장
    with open(jsonPath, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
