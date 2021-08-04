import { Component } from '@angular/core'
import { AuthActions, AuthState } from '@/auth/store'
import { Store } from '@ngrx/store'
import { RequestRegistration, RequestRegistrationSchool, TypeUserType, TypeUserTypeSchool } from '@/auth/models'
import { Agreements } from '@/auth/models/agreements'


@Component( {
    selector: 'app-register',
    templateUrl: './register.component.html',
    styleUrls: [ './register.component.scss' ]
} )
export class RegisterComponent
{
    agreements: string[] = Agreements
    registerTypes: TypeUserTypeSchool[] = [ TypeUserTypeSchool.PreUniversity, TypeUserTypeSchool.School, TypeUserTypeSchool.Enrollee ]

    registerAttempt: RequestRegistration // TODO switch to RequestRegistration
    isRegistered: boolean

    selectedUserType: TypeUserType | null
    hasRegisterNumber: boolean
    agreementAccepted: boolean

    constructor( private readonly store: Store<AuthState.State> )
    {
        this.registerAttempt = {
            authInfo: { email: '', password: '' },
            registerType: this.registerTypes[ 0 ],
            personalInfo: { dateOfBirth: '', firstName: '', secondName: '', middleName: '' },
            registerConfirm: { registrationNumber: '', password: '' }
        }
        this.isRegistered = false
        this.agreementAccepted = false
        this.selectedUserType = null
        this.hasRegisterNumber = false
    }

    selectRegisterType( userType: TypeUserTypeSchool ): void
    {
        this.selectedUserType = userType
    }

    isAvailable(): boolean
    {
        return this.selectedUserType !== null && this.selectedUserType == TypeUserTypeSchool.School
    }

    isValid( registration: RequestRegistration ): boolean
    {
        return this.agreementAccepted
    }

    register( registerUser: RequestRegistration ): void
    {
        this.isRegistered = true
        this.store.dispatch( AuthActions.registerAttempt( { requestRegistration: registerUser } ) )
    }
}
