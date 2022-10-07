import pickle
from fastapi import FastAPI, File, UploadFile 
from fastapi.responses import StreamingResponse
from io import StringIO
import pandas as pd

app = FastAPI()
model_file = "model.sav"

@app.post("/predict")
async def predict(csv_file: UploadFile = File(...)):
    #入力
    csvdata = StringIO(str(csv_file.file.read(), 'utf-8'))
    df = pd.read_csv(csvdata)
    model = pickle.load(open(model_file, 'rb'))

    #データの前処理
    df = preprocessing(df)
    X = df.values

    #予測
    y_pred = model.predict(X)
    df_y_pred = pd.DataFrame(data=y_pred, columns=["pred"])

    #出力
    stream = StringIO()
    df_y_pred.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=predict.csv"

    return response

def preprocessing(df: pd):
    #Base_Planを数値データに変換
    df["Base_Plan"] = df["Base_Plan"].replace("light", 0)
    df["Base_Plan"] = df["Base_Plan"].replace("normal", 1)
    df["Base_Plan"] = df["Base_Plan"].replace("premium", 2)

    #Opponent_Planを数値データに変換
    df["Opponent_Plan"] = df["Opponent_Plan"].replace("light", 0)
    df["Opponent_Plan"] = df["Opponent_Plan"].replace("normal", 1)
    df["Opponent_Plan"] = df["Opponent_Plan"].replace("premium", 2)

    #Dating_Days__dating_dateを数値データに変換
    df["Dating_Days__dating_date"] = df["Dating_Days__dating_date"].str.replace("/","").astype(int)

    #Dating_Days__slotを数値データに変換
    df["Dating_Days__slot"] = df["Dating_Days__slot"].replace("lunch_time", 0)
    df["Dating_Days__slot"] = df["Dating_Days__slot"].replace("evening_time", 1)

    return df