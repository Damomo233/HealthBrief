import json
import time

from backend.services.router import route_question


with open(
    "evaluation/questions.json",
    "r",
    encoding="utf-8"
) as file:

    dataset = json.load(file)


correct = 0

total_time = 0


for item in dataset:

    question = item["question"]

    expected = item["expected_category"]


    start = time.perf_counter()


    result = route_question(
        question
    )


    end = time.perf_counter()


    predicted = result["category"]


    elapsed = end - start

    total_time += elapsed


    if predicted == expected:

        correct += 1

        status = "PASS"

    else:

        status = "FAIL"


    print(
        f"{status} | "
        f"Expected: {expected} | "
        f"Predicted: {predicted}"
    )

    print(
        f"Question: {question}"
    )

    print()


accuracy = correct / len(dataset)

average_latency = total_time / len(dataset)


print("----------------------")

print(
    f"Category Accuracy: "
    f"{accuracy:.2%}"
)

print(
    f"Average Router Latency: "
    f"{average_latency:.2f} seconds"
)

