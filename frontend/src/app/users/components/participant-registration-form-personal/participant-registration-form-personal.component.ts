import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { Gender, ParticipantRegister } from '@/users/models/participant'
import { ParticipantService } from '@/users/services/participant.service'
import { select, Store } from '@ngrx/store'
import { AuthSelectors, AuthState } from '@/auth/store'
import { CommonUserInfo, PersonalInfo } from '@/auth/models'
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
    commonUserInfo$!: Observable<CommonUserInfo | null>
    personalInfo$!: Observable<PersonalInfo | null>


    constructor( private service: ParticipantService, private store: Store<AuthState.State> )
    {
    }

    ngOnInit(): void
    {
        this.countriesList = this.service.getCountriesList()
        this.commonUserInfo$ = this.store.pipe( select( AuthSelectors.selectCommonUserInfo ) )
        this.personalInfo$ = this.store.pipe( select( AuthSelectors.selectPersonalInfo ) )
    }
}
