import pickle
from fastapi import FastAPI, File, UploadFile 
from fastapi.responses import StreamingResponse
from io import StringIO
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = FastAPI()
model_file = "classifier_model.sav"

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
    #予測確率
    y_pred_prob = model.predict_proba(X)
    df_pred_prob = pd.DataFrame({'pred':y_pred, 'low_satisfaction_prob':y_pred_prob[:,0], 'high_satisfaction_prob':y_pred_prob[:,1]})

    #出力
    stream = StringIO()
    df_pred_prob.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=predict.csv"

    return response

def preprocessing(df: pd):
    #特徴量抜粋
    df = df[["Base_face_point_difference",\
        "Opponent_face_point_difference",\
        "Opponent_for_last_satisfaction_avg",\
        "Opponent_for_face_points_avg",\
        "Opponent_for_personality_points_avg",\
        "Opponent_for_b_suitable_avg"]]

    #標準化
    std = StandardScaler()
    df["Base_face_point_difference"] = std.fit_transform(df[["Base_face_point_difference"]])
    df["Opponent_face_point_difference"] = std.fit_transform(df[["Opponent_face_point_difference"]])
    df["Opponent_for_last_satisfaction_avg"] = std.fit_transform(df[["Opponent_for_last_satisfaction_avg"]])
    df["Opponent_for_face_points_avg"] = std.fit_transform(df[["Opponent_for_face_points_avg"]])
    df["Opponent_for_personality_points_avg"] = std.fit_transform(df[["Opponent_for_personality_points_avg"]])
    df["Opponent_for_b_suitable_avg"] = std.fit_transform(df[["Opponent_for_b_suitable_avg"]])

    return df