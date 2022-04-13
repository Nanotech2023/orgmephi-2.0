import { Component } from '@angular/core'
import { Observable, of } from 'rxjs'
import { ActivatedRoute, Router } from '@angular/router'
import { catchError, filter, map, tap } from 'rxjs/operators'
import { UsersService } from '@api/users/users.service'
import { ResetPasswordUser } from '@api/users/models'
import { displayErrorMessage, displaySuccessMessage } from '@/shared/logging'


@Component( {
    selector: 'app-reset-password-request-success',
    templateUrl: './reset-password-request-success.component.html',
    styleUrls: [ './reset-password-request-success.component.scss' ]
} )
export class ResetPasswordRequestSuccessComponent
{
    token$!: Observable<string>
    newPasswordConfirmValue: string = ""
    newPasswordValue: string = ""

    constructor( private usersService: UsersService, private route: ActivatedRoute, private router: Router ) { }

    ngOnInit(): void
    {
        this.token$ = this.route.queryParams.pipe(
            filter( params => params.token ),
            map( params => params.token )
        )
    }

    onSubmit( token: string ): void
    {
        const resetPasswordUser: ResetPasswordUser = { password: this.newPasswordValue }
        this.usersService.userRegistrationRecoverTokenPost( token, resetPasswordUser ).pipe(
            tap( () => of( displaySuccessMessage( "Пароль успешно изменён" ) ) ),
            catchError( ( error: any ) => of( displayErrorMessage( error ) ) ),
            tap( () => this.router.navigate( [ '/auth/login' ] ) )
        ).subscribe()
    }
}
