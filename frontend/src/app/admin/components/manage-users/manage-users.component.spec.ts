import { ComponentFixture, TestBed } from '@angular/core/testing'

import { ManageUsersComponent } from './manage-users.component'
import { AuthService } from '@/auth/api/auth.service'
import { ResponseUserAll, TypeUserRole, TypeUserType } from '@/auth/api/models'
import { Observable, of } from 'rxjs'


describe( 'ManageUsersComponent', () =>
{
    let component: ManageUsersComponent
    let fixture: ComponentFixture<ManageUsersComponent>
    let mockAuthService: { userAllGet: { and: { returnValue: ( arg0: Observable<ResponseUserAll> ) => void } } }
    let users: ResponseUserAll

    beforeEach( async () =>
    {
        mockAuthService = jasmine.createSpyObj( [ 'userAllGet' ] )

        await TestBed.configureTestingModule( {
            declarations: [ ManageUsersComponent ],
            providers: [
                { provide: AuthService, useValue: mockAuthService }
            ]
        } ).compileComponents()
    } )

    beforeEach( () =>
    {
        fixture = TestBed.createComponent( ManageUsersComponent )
        component = fixture.componentInstance
        fixture.detectChanges()
    } )

    it( 'should create', () =>
    {
        expect( component ).toBeTruthy()
    } )

    it( 'should set users correctly from the service', () =>
    {
        users = {
            users: [
                { id: 1, role: TypeUserRole.Creator, type: TypeUserType.Internal, username: "Проректор" },
                { id: 2, role: TypeUserRole.Participant, type: TypeUserType.School, username: "Студент 1" },
                { id: 3, role: TypeUserRole.Participant, type: TypeUserType.School, username: "Студент 2" }
            ]
        }
        mockAuthService.userAllGet.and.returnValue( of( users ) )
        fixture.whenStable().then( () =>
        {
            fixture.componentInstance.users$.subscribe( ( item: ResponseUserAll ) =>
                expect( item.users.length ).toBe( 3 ) )
        } )
    } )
} )