import { Component, OnInit } from '@angular/core'
import { UsersService } from '@api/users/users.service'
import { Router } from '@angular/router'


@Component( {
    selector: 'app-reset-password',
    templateUrl: './reset-password.component.html',
    styleUrls: [ './reset-password.component.scss' ]
} )
export class ResetPasswordComponent
{
    emailToReset: string = ""

    constructor( private usersService: UsersService, private router: Router )
    {
    }

    onSubmit(): void
    {
        this.usersService.userRegistrationForgotEmailPost( this.emailToReset )
        this.router.navigate( [ "/reset-password/confirm" ], { queryParams: { email: this.emailToReset } } )
    }
}