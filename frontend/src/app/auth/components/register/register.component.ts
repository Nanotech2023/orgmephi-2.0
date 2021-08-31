import { Component } from '@angular/core'
import { AuthActions, AuthState } from '@/auth/store'
import { Store } from '@ngrx/store'
import { SchoolRegistrationRequestUser } from '@/auth/api/models'
import { Agreements } from '@/auth/agreements'


@Component( {
    selector: 'app-register',
    templateUrl: './register.component.html',
    styleUrls: [ './register.component.scss' ]
} )
export class RegisterComponent
{
    agreements: string[] = Agreements
    registerTypes: SchoolRegistrationRequestUser.RegisterTypeEnum[] = [ SchoolRegistrationRequestUser.RegisterTypeEnum.PreUniversity, SchoolRegistrationRequestUser.RegisterTypeEnum.School, SchoolRegistrationRequestUser.RegisterTypeEnum.Enrollee ]

    registerAttempt: SchoolRegistrationRequestUser // TODO support RequestRegistrationUniversity
    isRegistered: boolean

    selectedUserType: SchoolRegistrationRequestUser.RegisterTypeEnum | null
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

    selectRegisterType( userType: SchoolRegistrationRequestUser.RegisterTypeEnum ): void
    {
        this.selectedUserType = userType
    }

    isAvailable(): boolean
    {
        return this.selectedUserType !== null && this.selectedUserType == SchoolRegistrationRequestUser.RegisterTypeEnum.School
    }

    isValid( registration: SchoolRegistrationRequestUser ): boolean
    {
        return this.agreementAccepted
    }

    register( registerUser: SchoolRegistrationRequestUser ): void
    {
        this.isRegistered = true
        this.store.dispatch( AuthActions.registerRequest( { registrationRequestUser: registerUser } ) )
    }
}
