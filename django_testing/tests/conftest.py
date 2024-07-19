import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django.urls import reverse
from students.models import Course


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make(Course, **kwargs)

    return factory


@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    course = course_factory()
    url = reverse('course-detail', args=[course.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == course.id


@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    courses = course_factory(_quantity=3)
    url = reverse('course-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3


@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    courses = course_factory(_quantity=3)
    course = courses[0]
    url = reverse('course-list')
    response = api_client.get(url, {'id': course.id})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == course.id


@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    courses = course_factory(_quantity=3)
    course = courses[0]
    url = reverse('course-list')
    response = api_client.get(url, {'name': course.name})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == course.name


@pytest.mark.django_db
def test_create_course(api_client):
    url = reverse('course-list')
    data = {
        'name': 'New Course',
        'description': 'Course Description'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert Course.objects.filter(name='New Course').exists()


@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course = course_factory()
    url = reverse('course-detail', args=[course.id])
    data = {
        'name': 'Updated Course',
        'description': 'Updated Description'
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == 200
    course.refresh_from_db()
    assert course.name == 'Updated Course'
    assert course.description == 'Updated Description'


@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory()
    url = reverse('course-detail', args=[course.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Course.objects.filter(id=course.id).exists()
