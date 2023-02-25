from flask import jsonify,request,session, Flask
from marshmallow import ValidationError
from models import User, Workout, Payment, Subscription, Video
from  api import api
from item import StreaksSchema, UserSchema, WorkoutSchema, PaymetSchema, SubscriptionSchema, VideoSchema
from flask_restful import Resource
from flask_bcrypt import bcrypt
import re
from config import * 

USER_NOT_FOUND = "User not found."
WORKOUT_NOT_FOUND = "Workout not found."
PAYMENT_NOT_FOUND = "Payment not found."
SUBSCRIPTION_NOT_FOUND = "Subscription not found."
VIDEO_NOT_FOUND = "Video not found."

# Initialize schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Initialize schema
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

# Initialize schema
payment_schema = PaymetSchema()
payments_schema = PaymetSchema(many=True)

# Initialize schema
subscription_schema = SubscriptionSchema()
subscriptions_schema = SubscriptionSchema(many=True)

# Initialize schema
video_schema = VideoSchema()
videos_schema = VideoSchema(many=True)

#initialize schema
streak_schema = StreaksSchema()
streaks_schema = StreaksSchema(many=True)


@api.resource("/users")
class UserList(Resource):
    def get():
        return users_schema.dump(User.find_all()), 200

    def put(id):
        user_json = request.get_json()
        if not user_json:
            return {'message': "No input data provided"}, 400
        try:
            user_data = user_schema.load(user_json)
            if not re.match(r'[^@]+@[^@]+\.[^@]+', user_data.email):
                return 'Invalid email', 400
        except ValidationError as err:
            return err.messages, 422
        user = User.find_by_id(id)
        if not user:
            return {'message': USER_NOT_FOUND}, 404
        user.email = user_data.email
        user.fullname = user_data.fullname
        user.phoneNumber = user_data.phoneNumber
        user.password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
        user.save_to_db()
        return user_schema.dump(user), 200

    
    def delete():
        users_to_delete = User.find_by_id(id)
        users_to_delete.delete_from_db()
        return jsonify({"message":"User Deleted Successfully"}),204

@api.resource("/user", "/user/<int:id>")
class Users(Resource):
    def post():
        user_json= request.get_json()
        if not user_json:
            return {'message': 'No input data provided'}, 400
            # Validate and deserialize input
        try:
            user_data = user_schema.load(user_json)
        except ValidationError as err:
            return err.messages, 422
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
        user = User(fullname=user_data.fullname, email=user_data.email, phoneNumber=user_data.phoneNumber, password=hashed_password)
        user.save_to_db()
        return user_schema.dump(user), 201

    def get(id):
        user_data = User.find_by_id(id)
        if user_data:
            return user_schema.dump(user_data)
        return {'message': USER_NOT_FOUND}, 404


    def put():
        user_json = request.get_json()
        if not user_json:
            return {'message':"No input data provided"}, 400
        try:
            user_data = user_schema.load(user_json)
            if not re.match(r'[^@]+@[^@]+\.[^@]+', user_data.email):
                return 'Invalid email', 400
        except ValidationError as err:
            return err.messages, 422
        hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
        user = User(fullname=user_data.fullname, email=user_data.email, phoneNumber=user_data.phoneNumber, password=hashed_password)
        user.save_to_db()
        return user_schema.dump(user), 200

    def delete(id):
        users_to_delete = User.find_by_id(id)
        users_to_delete.delete_from_db()
        return jsonify({"message":"User Deleted Successfully"}), 204


@api.resource("/workouts", "/workouts/<id>")
class Workouts(Resource):
    def get(id):
        workout = Workout.find_by_id(id)
        if not workout:
            return {'message': 'workout not found'}, 404
        return workout_schema.dump(workout)
        # (Workout.find_all()), 200

    def post():
        workout_json = request.get_json()
        workout_data = workout_schema.load(workout_json)
        workout_data.save_to_db()
        return workout_schema.dump(workout_data), 200

    def delete(id):
        workout_data = Workout.find_by_id(id)
        if workout_data:
            workout_data.delete_from_db()
            return {'message': "Workout Deleted successfully"}, 200
        return {'status': WORKOUT_NOT_FOUND}
    
    def put(id):
        workout_data = request.get_json()
        if not workout_data:
            return {'message': "No input data provided"}, 400
        try:
            workout = Workout.find_by_id(id)
            if not workout:
                return {'message': WORKOUT_NOT_FOUND}, 404
            workout_data = workout_schema.load(workout_data)
            workout.title = workout_data.title
            workout.description = workout_data.description
            workout.duration = workout_data.duration
            workout.save_to_db()
            return workout_schema.dump(workout), 200
        except ValidationError as err:
            return err.messages, 422



@api.resource("/payment")
class Payments(Resource):
    def get(id):
        payment = Payment.find_by_id(id)
        if not payment:
            return {'message': 'Payment not found'}, 404
        return payment_schema.dump(payment), 200        

    def post():
        payment_json = request.get_json()
        payment_data = payment_schema.load(payment_json)
        payment_data.save_to_db()
        return payment_schema.dump(payment_data), 200
    

    def put():
        payment_json = request.get_json()
        payment_data = payment_schema.load(payment_json)
        payment = Payment.find_by_id(payment_data.id)
        if not payment:
            return {'message': 'Payment not found'}, 404
        payment.save_to_db()
        return payment_schema.dump(payment_data), 200

    def delete(id):
        payment_to_delete = Payment.find_by_id(id)
        payment_to_delete.delete_from_db()
        return jsonify({"message":"Payment Deleted Successfully"}),204

@api.resource("/subscriprtion")
class Subscriptions(Resource):
    def get(id):
        subscription = Subscription.find_by_id(id)
        if not subscription:
            return {'message': 'Subscription not found'}, 404
        return subscription_schema.dump(subscription), 200

    def post():
        subscription_json = request.get_json()
        subscription_data = subscription_schema.load(subscription_json)
        subscription_data.save_to_db()
        return subscription_schema.dump(subscription_data), 200

    def put():
        subscription_json = request.get_json()
        subscription_data = subscription_schema.load(subscription_json)
        subscription = Subscription.find_by_id(subscription_data.id)
        if not subscription:
            return {'message': 'Subscription not found'}, 404
        subscription.save_to_db()
        return subscription_schema.dump(subscription_data), 200

    def delete(id):
        subscription_to_delete = Subscription.find_by_id(id)
        subscription_to_delete.delete_from_db()
        return jsonify({"message":"Subscription Deleted Successfully"}),204


@api.resource("/video")
class Videos(Resource):
    def get(id):
        video = Video.find_by_id(id)
        if not video:
            return {'message': 'Video not found'}, 404
        return video_schema.dump(video), 200
    
    def post():
        video_json = request.get_json()
        video_data = video_schema.load(video_json)
        video_data.save_to_db()
        return video_schema.dump(video_data), 200

    def put():
        video_json = request.get_json()
        video_data = video_schema.load(video_json)
        video = Video.find_by_id(video_data.id)
        if not video:
            return {'message': 'Video not found'}, 404
        video.save_to_db()
        return video_schema.dump(video_data), 200

    def delete(id):
        video_to_delete = Video.find_by_id(id)
        video_to_delete.delete_from_db()
        return jsonify({"message":"Video Deleted Successfully"}),204

@api.resource('/streaks')
class Streak(Resource):
    def get():
        return streaks_schema.dump(Streak.find_all()), 200
    
    def post():
        streak_json = request.get_json()
        streak_data = streak_schema.load(streak_json)
        streak_data.save_to_db()
        return streak_schema.dump(streak_data), 200

    def delete():
        Streak.delete_all()
        return jsonify({"message":"All St"})

    
    def post(self):
        json_data = request.get_json()
        data, errors = streak_schema.load(json_data)
        if errors:
            return errors, 422
        user_id = json_data.get("user_id")
        date = data.get("date")
        # Save the date to the database for the given user
        date.save_to_db()
        user_id.save_to_db()
        # save_date_to_db(user_id, date)
        # Fetch the dates from the database for the given user
        dates = user_id.find_all()
        # dates = get_dates_from_db(user_id)
        # Sort the dates in chronological order
        dates.sort()
        streak = 0
        current_streak = 0
        for i in range(len(dates)):
            if i == 0:
                current_streak += 1
            else:
                previous_date = dates[i-1]
                current_date = dates[i]
                if (current_date - previous_date).days == 1:
                    current_streak += 1
                else:
                    streak = max(streak, current_streak)
                    current_streak = 0
        return {"streak": max(streak, current_streak)}

def save_date_to_db(user_id, date):
    # Save the date to the database for the given user
    pass

def get_dates_from_db(user_id):
    # Fetch the dates from the database for the given user
    # Example: dates = [datetime(2022, 1, 1), datetime(2022, 1, 2), datetime(2022, 1, 3)]
    # return dates
    pass