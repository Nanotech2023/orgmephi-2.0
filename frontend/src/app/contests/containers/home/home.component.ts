import { Component } from '@angular/core'
import { Observable } from 'rxjs'
import { UserInfo } from '@api/users/models'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { UsersService } from '@api/users/users.service'


@Component( {
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: [ './home.component.scss' ]
} )
export class HomeComponent
{
    personalInfo$: Observable<UserInfo>

    constructor( private authStore: Store<AuthState.State>, private usersService: UsersService )
    {
        this.personalInfo$ = this.authStore.pipe( select( AuthSelectors.selectUserInfo ) )
    }

    download()
    {
        this.usersService.userProfileCardGet().subscribe( data => this.downloadFile( data ) )
    }

    downloadFile( data: Blob )
    {
        const blob = new Blob( [ data ], { type: 'application/pdf' } )
        const url = window.URL.createObjectURL( blob )
        window.open( url )
    }
}
