import { Component, OnInit } from '@angular/core'
import { RegisterType, RegisterTypeEnum, RegisterTypes, UserRegister, validateUser } from '@/auth/models'
import { AuthService } from '@/auth/services/auth.service'
import { RegisterResult } from '@/auth/models/registerResult'


@Component( {
    selector: 'app-register',
    templateUrl: './register.component.html',
    styleUrls: [ './register.component.scss' ]
} )
export class RegisterComponent implements OnInit
{
    registerUser: UserRegister
    registerTypes: RegisterType[] = RegisterTypes
    selectedRegisterType: RegisterType | null
    hasRegisterNumber: boolean
    agreementAccepted: boolean
    registerResult: RegisterResult | null
    registrationCompleted: boolean

    constructor( private service: AuthService )
    {
        this.registerUser = {
            registerNumber: '',
            activationCode: '',
            email: '',
            password: '',
            name: '',
            lastName: '',
            birthDate: null,
            surname: ''
        }
        this.agreementAccepted = false
        this.selectedRegisterType = null
        this.hasRegisterNumber = false
        this.registerResult = null
        this.registrationCompleted = false
    }

    ngOnInit(): void
    {
    }

    selectRegisterType( registerType: RegisterType )
    {
        this.selectedRegisterType = registerType
    }

    isAvailable()
    {
        return this.selectedRegisterType !== null && this.selectedRegisterType?.value == RegisterTypeEnum.schoolOlymp
    }

    isValid()
    {
        return validateUser( this.registerUser ) && this.agreementAccepted
    }

    register()
    {
        this.registerResult = this.service.register( this.registerUser )
        this.registrationCompleted = true
    }
}
