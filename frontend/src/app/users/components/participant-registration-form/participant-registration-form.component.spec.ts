import { ComponentFixture, TestBed } from '@angular/core/testing'

import { ParticipantRegistrationFormComponent } from './participant-registration-form.component'


describe( 'ParticipantRegistrationFormComponent', () =>
{
    let component: ParticipantRegistrationFormComponent
    let fixture: ComponentFixture<ParticipantRegistrationFormComponent>

    beforeEach( async () =>
    {
        await TestBed.configureTestingModule( {
            declarations: [ ParticipantRegistrationFormComponent ]
        } )
            .compileComponents()
    } )

    beforeEach( () =>
    {
        fixture = TestBed.createComponent( ParticipantRegistrationFormComponent )
        component = fixture.componentInstance
        fixture.detectChanges()
    } )

    it( 'should create', () =>
    {
        expect( component ).toBeTruthy()
    } )
} )
