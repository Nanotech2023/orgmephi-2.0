import { ComponentFixture, TestBed } from '@angular/core/testing'

import { ParticipantRegistrationFormPersonalComponent } from './participant-registration-form-personal.component'


describe( 'ParticipantRegistrationFormPersonalComponent', () =>
{
    let component: ParticipantRegistrationFormPersonalComponent
    let fixture: ComponentFixture<ParticipantRegistrationFormPersonalComponent>

    beforeEach( async () =>
    {
        await TestBed.configureTestingModule( {
            declarations: [ ParticipantRegistrationFormPersonalComponent ]
        } )
            .compileComponents()
    } )

    beforeEach( () =>
    {
        fixture = TestBed.createComponent( ParticipantRegistrationFormPersonalComponent )
        component = fixture.componentInstance
        fixture.detectChanges()
    } )

    it( 'should create', () =>
    {
        expect( component ).toBeTruthy()
    } )
} )
