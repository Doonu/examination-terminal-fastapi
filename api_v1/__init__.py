from fastapi import APIRouter

from .auth.views import router as auth_router
from .role.views import router as role_router
from .profile.views import router as profile_router
from .course.views import router as course_router
from .course_test.views import router as test_router
from .questions.views import router as question_router
from .test_progress.views import router as test_progress_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth")
router.include_router(role_router, prefix="/role")
router.include_router(profile_router, prefix="/profile")
router.include_router(course_router, prefix="/course")
router.include_router(test_router, prefix="/tests")
router.include_router(question_router, prefix="/questions")
router.include_router(test_progress_router, prefix="/test-progress")
