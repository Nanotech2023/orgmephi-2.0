import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { User, UserInfo } from '@api/users/models'
import { Observable } from 'rxjs'


@Component( {
    selector: 'app-participant-registration-form-personal',
    templateUrl: './participant-registration-form-personal.component.html',
    styleUrls: [ './participant-registration-form-personal.component.scss' ]
} )
export class ParticipantRegistrationFormPersonalComponent implements OnInit
{
    @Input() participant!: ParticipantRegister
    @Output() participantChange: EventEmitter<ParticipantRegister> = new EventEmitter<ParticipantRegister>()

    genderOptions: Gender[] = [ Gender.male, Gender.female ]
    countriesList: string[] = []
    user$!: Observable<User | null>
    userInfo$!: Observable<UserInfo | null>


    constructor( private service: ParticipantService, private store: Store<AuthState.State> )
    {
    }

    ngOnInit(): void
    {
        this.countriesList = this.service.getCountriesList()
        this.user$ = this.store.pipe( select( AuthSelectors.selectUser ) )
        this.userInfo$ = this.store.pipe( select( AuthSelectors.selectUserInfo ) )
    }
}
