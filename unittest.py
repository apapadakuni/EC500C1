import APIEXERCISE
import time

def unit_test_odd_sizes():
    try:
        print(APIEXERCISE.to_movie("dannygarcia95"))
        print("Passed test: odd image sizes")
    except Exception as e:
        print("Failed test one with error")
        print(str(e))

def unit_test_bad_user():
    try:
        APIEXERCISE.to_movie("iuohgeriutohweortiuhwert")
        print("Failed test, accepted non-existent user")
    except Exception as e:
        print("Passed test: Nonexistent user")

def unit_test_no_media():
    try:
        APIEXERCISE.to_movie("OneTweetTony")
        print("Failed test, no media")
    except Exception as e:
        print("Passed test, name with no media")
        print(str(e))

def time_call():
	start = time.time()
	APIEXERCISE.to_movie("dannygarcia95")
	print("Took: ", time.time() - start, " seconds")


if __name__ == "__main__":

    unit_test_odd_sizes()
    unit_test_bad_user()
    unit_test_no_media()
    time_call()