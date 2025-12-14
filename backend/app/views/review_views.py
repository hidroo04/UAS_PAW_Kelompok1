"""
Review views for class ratings and feedback
"""
from pyramid.view import view_config
from pyramid.response import Response
import json
from datetime import datetime
from ..models import Review, GymClass, User, Booking
from ..utils.auth import get_token_from_header, decode_jwt_token


@view_config(route_name='api_class_reviews', renderer='json', request_method='GET')
def get_class_reviews(request):
    """Get all reviews for a specific class"""
    try:
        db = request.dbsession
        class_id = request.matchdict['id']
        
        # Check if class exists
        gym_class = db.query(GymClass).filter(GymClass.id == class_id).first()
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found'}),
                status=404,
                content_type='application/json'
            )
        
        # Get all reviews
        reviews = db.query(Review).filter(Review.class_id == class_id).all()
        
        reviews_data = [r.to_dict() for r in reviews]
        
        # Calculate average rating
        average_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
        
        return {
            'status': 'success',
            'data': {
                'class_id': class_id,
                'class_name': gym_class.name,
                'reviews': reviews_data,
                'total_reviews': len(reviews_data),
                'average_rating': round(average_rating, 2)
            }
        }
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_class_reviews', renderer='json', request_method='POST')
def create_review(request):
    """Create a new review for a class"""
    try:
        # Check authentication
        token = get_token_from_header(request)
        if not token:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json'
            )
        
        payload = decode_jwt_token(token)
        user_id = payload.get('user_id')
        
        db = request.dbsession
        class_id = request.matchdict['id']
        data = request.json_body
        
        # Validation
        if 'rating' not in data:
            return Response(
                json.dumps({'status': 'error', 'message': 'Rating is required'}),
                status=400,
                content_type='application/json'
            )
        
        rating = float(data['rating'])
        if rating < 1.0 or rating > 5.0:
            return Response(
                json.dumps({'status': 'error', 'message': 'Rating must be between 1.0 and 5.0'}),
                status=400,
                content_type='application/json'
            )
        
        # Check if class exists
        gym_class = db.query(GymClass).filter(GymClass.id == class_id).first()
        if not gym_class:
            return Response(
                json.dumps({'status': 'error', 'message': 'Class not found'}),
                status=404,
                content_type='application/json'
            )
        
        # Check if user has booked this class
        booking = db.query(Booking).filter(
            Booking.class_id == class_id,
            Booking.member_id == user_id
        ).first()
        
        if not booking:
            return Response(
                json.dumps({'status': 'error', 'message': 'You must book this class before reviewing'}),
                status=403,
                content_type='application/json'
            )
        
        # Check if user already reviewed
        existing_review = db.query(Review).filter(
            Review.class_id == class_id,
            Review.user_id == user_id
        ).first()
        
        if existing_review:
            return Response(
                json.dumps({'status': 'error', 'message': 'You have already reviewed this class'}),
                status=400,
                content_type='application/json'
            )
        
        # Create review
        new_review = Review(
            class_id=class_id,
            user_id=user_id,
            rating=rating,
            comment=data.get('comment', '')
        )
        
        db.add(new_review)
        db.commit()
        
        return {
            'status': 'success',
            'message': 'Review added successfully',
            'data': new_review.to_dict()
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_review', renderer='json', request_method='PUT')
def update_review(request):
    """Update an existing review"""
    try:
        # Check authentication
        token = get_token_from_header(request)
        if not token:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json'
            )
        
        payload = decode_jwt_token(token)
        user_id = payload.get('user_id')
        
        db = request.dbsession
        review_id = request.matchdict['id']
        data = request.json_body
        
        # Get review
        review = db.query(Review).filter(Review.id == review_id).first()
        
        if not review:
            return Response(
                json.dumps({'status': 'error', 'message': 'Review not found'}),
                status=404,
                content_type='application/json'
            )
        
        # Check ownership
        if review.user_id != user_id:
            return Response(
                json.dumps({'status': 'error', 'message': 'You can only update your own reviews'}),
                status=403,
                content_type='application/json'
            )
        
        # Update fields
        if 'rating' in data:
            rating = float(data['rating'])
            if rating < 1.0 or rating > 5.0:
                return Response(
                    json.dumps({'status': 'error', 'message': 'Rating must be between 1.0 and 5.0'}),
                    status=400,
                    content_type='application/json'
                )
            review.rating = rating
        
        if 'comment' in data:
            review.comment = data['comment']
        
        review.updated_at = datetime.utcnow()
        db.commit()
        
        return {
            'status': 'success',
            'message': 'Review updated successfully',
            'data': review.to_dict()
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )


@view_config(route_name='api_review', renderer='json', request_method='DELETE')
def delete_review(request):
    """Delete a review"""
    try:
        # Check authentication
        token = get_token_from_header(request)
        if not token:
            return Response(
                json.dumps({'status': 'error', 'message': 'Authentication required'}),
                status=401,
                content_type='application/json'
            )
        
        payload = decode_jwt_token(token)
        user_id = payload.get('user_id')
        role = payload.get('role')
        
        db = request.dbsession
        review_id = request.matchdict['id']
        
        # Get review
        review = db.query(Review).filter(Review.id == review_id).first()
        
        if not review:
            return Response(
                json.dumps({'status': 'error', 'message': 'Review not found'}),
                status=404,
                content_type='application/json'
            )
        
        # Check ownership or admin
        if review.user_id != user_id and role != 'ADMIN':
            return Response(
                json.dumps({'status': 'error', 'message': 'You can only delete your own reviews'}),
                status=403,
                content_type='application/json'
            )
        
        db.delete(review)
        db.commit()
        
        return {
            'status': 'success',
            'message': 'Review deleted successfully'
        }
        
    except Exception as e:
        return Response(
            json.dumps({'status': 'error', 'message': str(e)}),
            status=500,
            content_type='application/json'
        )
