from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student
import xml.etree.ElementTree as ET

def xml_response(data, status=200):
    return HttpResponse(data, content_type='application/xml', status=status)

@csrf_exempt
def create_student(request):
    if request.method == 'POST':
        try:
            tree = ET.fromstring(request.body)
            name = tree.find('name').text
            course = tree.find('course').text
            email = tree.find('email').text

            student = Student.objects.create(name=name, course=course, email=email)
            return xml_response(f'<student><id>{student.id}</id><name>{student.name}</name><course>{student.course}</course><email>{student.email}</email></student>', status=201)
        except Exception as e:
            return xml_response(f'<error>{str(e)}</error>', status=400)
    else:
        return xml_response('<error>Method not allowed</error>', status=405)
    
def list_students(request):
    students = Student.objects.all()
    root = ET.Element('students')
    for student in students:
        student_elem = ET.SubElement(root, 'student')
        ET.SubElement(student_elem, 'id').text = str(student.id)
        ET.SubElement(student_elem, 'name').text = student.name
        ET.SubElement(student_elem, 'course').text = student.course
        ET.SubElement(student_elem, 'email').text = student.email
    return xml_response(ET.tostring(root), status=200)



@csrf_exempt
def update_student(request, student_id):
    if request.method == 'PUT':
        try:
            student = Student.objects.get(id=student_id)
            tree = ET.fromstring(request.body)
            student.name = tree.find('name').text
            student.course = tree.find('course').text
            student.email = tree.find('email').text
            student.save()
            return xml_response(f'<student><id>{student.id}</id><name>{student.name}</name><course>{student.course}</course><email>{student.email}</email></student>', status=200)
        except Student.DoesNotExist:
            return xml_response(f'<error>Student with id {student_id} not found</error>', status=404)
        except Exception as e:
            return xml_response(f'<error>{str(e)}</error>', status=400)
    else:
        return xml_response('<error>Method not allowed</error>', status=405)
    

@csrf_exempt
def delete_student(request, student_id):
    if request.method == 'DELETE':
        try:
            student = Student.objects.get(id=student_id)
            student.delete()
            return xml_response(f'<message>Student with id {student_id} deleted</message>', status=200)
        except Student.DoesNotExist:
            return xml_response(f'<error>Student with id {student_id} not found</error>', status=404)
    else:
        return xml_response('<error>Method not allowed</error>', status=405)
    
    