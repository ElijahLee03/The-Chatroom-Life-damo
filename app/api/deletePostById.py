import json

def delete_post_by_time(json_file, target_time):
    # JSON 파일 읽기
    with open(json_file, 'r') as file:
        data = json.load(file)

    # time이 target_time인 게시물 찾기
    found_index = None
    for index, post in enumerate(data):
        if post.get('time') == target_time:
            found_index = index
            break

    if found_index is not None:
        # 찾은 게시물 삭제
        deleted_post = data.pop(found_index)
        print(f"Post with time '{target_time}' deleted:\n{deleted_post}")
    else:
        print(f"No post found with time '{target_time}'.")

    # 수정된 내용을 JSON 파일에 쓰기
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=2)

# # 예제 사용
# json_file_path = 'example.json'  # JSON 파일의 경로
# target_post_time_to_delete = '2024-01-13_00_42_34'  # 삭제할 게시물의 시간

# delete_post_by_time(json_file_path, target_post_time_to_delete)
