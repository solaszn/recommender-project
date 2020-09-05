from master import predict, predictSimilar
import eel 

eel.init('web')

# Function to call from script
@eel.expose
def recommend(industry, service, rating):
    new_test = predict(industry, service, rating)
    print("Random Forest Prediction : ", new_test)
    result = predictSimilar(new_test)
    exposable_list = []
    for key, value in result.items():
    	for platform in value:
    		exposable_list.append(platform)
    toWrite = industry + ", " + service + ", " + str(rating) + ", " + str(exposable_list)
    with open("sessiondata.txt", "a") as file:
    	file.write(" ".join(toWrite) + "\n")
    print("Recommendations : " + str(exposable_list))
    return exposable_list

print("Server listening on localhost:8000/proto.html")
eel.start('proto.html', size=(1100,900))


# width - 1000px
# height - 700px