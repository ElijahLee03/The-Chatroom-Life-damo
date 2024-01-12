import json

def modify_post_by_time(json_file, target_time, new_title , new_content):
    # JSON 파일 읽기
    with open(json_file, 'r') as file:
        data = json.load(file)

    # time이 target_time인 게시물 찾기
    found = False
    for post in data:
        if post.get('time') == target_time:
            post['title'] = new_title
            post['content'] = new_content
            found = True
            break

    if not found:
        print(f"No post found with time '{target_time}'.")

    # 수정된 내용을 JSON 파일에 쓰기
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=2)