import { Component, OnInit } from '@angular/core'
import { UsersService } from '@api/users/users.service'
import { Router } from '@angular/router'


@Component( {
    selector: 'app-reset-password',
    templateUrl: './reset-password-request.component.html',
    styleUrls: [ './reset-password-request.component.scss' ]
} )
export class ResetPasswordRequestComponent
{
    emailToReset: string = ""

    constructor( private usersService: UsersService, private router: Router ) { }

    onSubmit(): void
    {
        this.usersService.userRegistrationForgotEmailPost( this.emailToReset ).subscribe()
        this.router.navigate( [ "/reset-password/confirm" ], { queryParams: { email: this.emailToReset } } )
    }
}