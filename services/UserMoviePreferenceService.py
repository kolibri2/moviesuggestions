from repositories import UserMoviePreferenceRepository


class UserMoviePreferenceService:
    def __init__(self, user_movie_preferences_repo: UserMoviePreferenceRepository):
        self.user_movie_preferences_repo = user_movie_preferences_repo

    def add_user_preference(self, user_id, movie_id, user_preference):

        movie_title = self.user_movie_preferences_repo.add_user_preference(
            user_id, movie_id, user_preference
        )
        return movie_title

    def get_user_preferences(self, user_id, movie_id) -> int:
        return self.user_movie_preferences_repo.get_user_preference(user_id, movie_id)
