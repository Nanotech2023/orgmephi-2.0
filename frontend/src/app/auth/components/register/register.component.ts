import { Component } from '@angular/core'
import { AuthActions, AuthState } from '@/auth/store'
import { Store } from '@ngrx/store'
import { Agreements } from '@/auth/models/agreements'
import { AllUserTypes, Registration, UserType } from '@/auth/models'


@Component( {
    selector: 'app-register',
    templateUrl: './register.component.html',
    styleUrls: [ './register.component.scss' ]
} )
export class RegisterComponent
{
    agreements: string[] = Agreements
    registerTypes: UserType[] = AllUserTypes

    registerAttempt: Registration
    isRegistered: boolean

    selectedUserType: UserType | null
    hasRegisterNumber: boolean
    agreementAccepted: boolean

    constructor( private readonly store: Store<AuthState.State> )
    {
        this.registerAttempt = {
            authInfo: { email: '', password: '' },
            registerType: this.registerTypes[ 0 ],
            personalInfo: { dateOfBirth: '', firstName: '', secondName: '', middleName: '' },
            registerConfirm: { registrationNumber: '', oneTimePassword: '' }
        }
        this.isRegistered = false
        this.agreementAccepted = false
        this.selectedUserType = null
        this.hasRegisterNumber = false
    }

    selectRegisterType( userType: UserType ): void
    {
        this.selectedUserType = userType
    }

    isAvailable(): boolean
    {
        return this.selectedUserType !== null && this.selectedUserType == UserType.School
    }

    isValid( registration: Registration ): boolean
    {
        return this.agreementAccepted
    }

    register( registerUser: Registration ): void
    {
        this.isRegistered = true
        this.store.dispatch( AuthActions.registerAttempt( { registration: registerUser } ) )
    }
}
