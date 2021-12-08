import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { UserLimitations } from '@api/users/models'
import { FormBuilder, FormControl, FormGroup } from '@angular/forms'


@Component( {
    selector: 'app-profile-edit-limitations',
    templateUrl: './profile-edit-limitations.component.html',
    styleUrls: [ './profile-edit-limitations.component.scss' ]
} )
export class ProfileEditLimitationsComponent implements OnInit
{
    @Input() model!: UserLimitations
    @Output() modelChange = new EventEmitter<UserLimitations>()
    userLimitationsForm!: FormGroup

    constructor( private formBuilder: FormBuilder )
    {
    }

    ngOnInit(): void
    {
        this.userLimitationsForm = this.formBuilder.group( {
            hearing: this.model?.hearing ?? false,
            movement: this.model?.movement ?? false,
            sight: this.model?.sight ?? false
        } )
        this.userLimitationsForm.valueChanges.subscribe( val =>
        {
            this.modelChange.emit( val as UserLimitations )
        } )
    }
}