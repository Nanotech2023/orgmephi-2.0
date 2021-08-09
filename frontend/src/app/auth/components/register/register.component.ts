import { Component } from '@angular/core'
import { AuthActions, AuthState } from '@/auth/store'
import { Store } from '@ngrx/store'
import { RequestRegistrationSchool, TypeUserType, TypeUserTypeSchool } from '@/auth/api/models'
import { Agreements } from '@/auth/agreements'


@Component( {
    selector: 'app-register',
    templateUrl: './register.component.html',
    styleUrls: [ './register.component.scss' ]
} )
export class RegisterComponent
{
    agreements: string[] = Agreements
    registerTypes: TypeUserTypeSchool[] = [ TypeUserTypeSchool.PreUniversity, TypeUserTypeSchool.School, TypeUserTypeSchool.Enrollee ]

    registerAttempt: RequestRegistrationSchool // TODO support RequestRegistrationUniversity
    isRegistered: boolean

    selectedUserType: TypeUserType | null
    hasRegisterNumber: boolean
    agreementAccepted: boolean

    constructor( private readonly store: Store<AuthState.State> )
    {
        this.registerAttempt = {
            auth_info: { email: '', password: '' },
            register_type: this.registerTypes[ 0 ],
            personal_info: { first_name: '', second_name: '', middle_name: '', date_of_birth: '' },
            register_confirm: { registration_number: '', password: '' }
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

    isValid( registration: RequestRegistrationSchool ): boolean
    {
        return this.agreementAccepted
    }

    register( registerUser: RequestRegistrationSchool ): void
    {
        this.isRegistered = true
        this.store.dispatch( AuthActions.registerAttempt( { requestRegistration: registerUser } ) )
    }
}
