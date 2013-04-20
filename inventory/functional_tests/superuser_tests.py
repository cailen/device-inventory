'''Functional tests using WebTest'''

from django.contrib.auth.models import User
from django_webtest import WebTest
from nose.tools import *
from inventory.user.tests.factories import (UserFactory,
                                             LendeeFactory)
from inventory.devices.tests.factories import DeviceFactory
from inventory.devices.models import Device
from inventory.user.models import Experimenter, Reader

class TestASuperUser(WebTest):
    def setUp(self):
        self.admin = UserFactory(first_name="Alan", last_name="Admin")
        self.admin.is_superuser = True
        self.admin.save()

    def tearDown(self):
        pass

    def test_can_add_device(self):
        # Goes to root (already logged in)
        res = self.app.get('/', user=self.admin).follow()
        assert_equal(res.request.path, '/devices/')
        # There's an Add device button
        assert_in('Add device', res)
        res = res.click('Add device')
        assert_equal(res.request.path, '/devices/add/')
        assert_in('Add device', res)

        # Fills in form
        form = res.forms['device_form']
        form['name'] = 'iPad 4, 16GB, WiFi'
        form['description'] = 'This is an Apple product.'
        form['responsible_party'] = 'Freddy Douglass'
        form['make'] = 'SERW09302'
        # forgets to put serial number
        # submits
        res = form.submit()
        # error message is displayed
        assert_in('This field is required', res)
        # enters serial number
        form['serial_number'] = '12345X67'
        # submits
        res = form.submit().follow()
        # device is saved to database
        assert_equal(Device.objects.all().count(), 1)
        # redirected to device index
        assert_equal(res.request.path, '/devices/')
        # the new device's name, status, Lender/Lendee, serial number is displayed
        # headers
        res.mustcontain('Name', 'Status', 'Lender', 'Lent to', 'Serial number')
        res.mustcontain('iPad 4, 16GB, WiFi', 'Storage', '12345X67')


    def test_can_see_delete_btn(self):
        # 3 devices are created
        device1, device2, device3 = DeviceFactory(), DeviceFactory(), DeviceFactory()
        assert_equal(Device.objects.all().count(), 3)
        # user goes to index page
        res = self.app.get('/', user=self.admin).follow()
        # devices are listed
        assert_in(device1.serial_number, res)
        assert_in(device2.serial_number, res)
        # there is a delete button
        assert_in('Delete', res)
        # selects first two devices

    def test_can_create_experimenter(self):
        # logs in 
        res = self.app.get('/', user=self.admin).follow()
        # Clicks on create new user
        res = res.click('Create user')
        # Fills out form to create a new user
        form = res.forms['user_form']
        # Sets the user type
        form.set('user_type', 'experimenter')
        form['first_name'] = 'Jimmy'
        form['last_name'] = 'Page'
        form['email'] = 'jimmy@example.com'
        form['password1'] = 'ledzep12'
        form['password2'] = 'ledzep12'
        # Submits
        res = form.submit().follow()
        # Back at the devices page
        assert_equal(res.request.path, '/devices/')
        # Sees success message
        assert_in('Successfully created user: jimmy@example.com', res)
        # User is saved to database
        assert_equal(Experimenter.objects.all().count(), 1)
        new_experimenter = Experimenter.objects.get(user__username='jimmy@example.com')
        assert_equal(new_experimenter.user.get_full_name(), 'Jimmy Page')

    def test_can_create_reader(self):
        # logs in 
        res = self.app.get('/', user=self.admin).follow()
        # Clicks on create new user
        res = res.click('Create user')
        # Fills out form to create a new user
        form = res.forms['user_form']
        # Sets the user type
        form.set('user_type', 'reader')
        form['first_name'] = 'Jimmy'
        form['last_name'] = 'Page'
        form['email'] = 'jimmy@example.com'
        form['password1'] = 'ledzep12'
        form['password2'] = 'ledzep12'
        # Submits
        res = form.submit().follow()
        # Back at the devices page
        assert_equal(res.request.path, '/devices/')
        # Sees success message
        assert_in('Successfully created user: jimmy@example.com', res)
        # User is saved to database
        assert_equal(Reader.objects.all().count(), 1)
        new_reader = Reader.objects.get(user__username='jimmy@example.com')
        assert_equal(new_reader.user.get_full_name(), 'Jimmy Page')

    def test_can_create_admin(self):
        # logs in 
        res = self.app.get('/', user=self.admin).follow()
        # Clicks on create new user
        res = res.click('Create user')
        # Fills out form to create a new user
        form = res.forms['user_form']
        # Sets the user type
        form.set('user_type', 'admin')
        form['first_name'] = 'Jimmy'
        form['last_name'] = 'Page'
        form['email'] = 'jimmy@example.com'
        form['password1'] = 'ledzep12'
        form['password2'] = 'ledzep12'
        # Submits
        res = form.submit().follow()
        # Back at the devices page
        assert_equal(res.request.path, '/devices/')
        # Sees success message
        assert_in('Successfully created user: jimmy@example.com', res)
        # User is saved to database
        new_admin = User.objects.get(username='jimmy@example.com')
        assert_equal(new_admin.get_full_name(), 'Jimmy Page')
        assert_true(new_admin.is_superuser)