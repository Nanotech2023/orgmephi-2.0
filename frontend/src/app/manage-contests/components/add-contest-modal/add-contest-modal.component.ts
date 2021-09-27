import { Component, ElementRef, EventEmitter, Input, Output, ViewChild } from '@angular/core'
import { BaseContest, CreateBaseOlympiadRequestTaskCreator } from '@api/tasks/model'
import SubjectEnum = BaseContest.SubjectEnum


@Component( {
    selector: 'app-add-contest-modal',
    templateUrl: './add-contest-modal.component.html',
    styleUrls: [ './add-contest-modal.component.scss' ],
    host: {
        '(document:click)': 'onClick($event)'
    }
} )
export class AddContestModalComponent
{
    @Input() modalVisible!: boolean
    @Output() modalVisibleChange: EventEmitter<boolean> = new EventEmitter<boolean>()
    @Output() addClick: EventEmitter<CreateBaseOlympiadRequestTaskCreator> = new EventEmitter<CreateBaseOlympiadRequestTaskCreator>()
    @ViewChild( 'modal' ) modal!: ElementRef

    createBaseOlympiadRequestTaskCreator: CreateBaseOlympiadRequestTaskCreator
    isCreated: boolean

    constructor()
    {
        this.createBaseOlympiadRequestTaskCreator = {
            diploma_1_condition: 9,
            diploma_2_condition: 8,
            diploma_3_condition: 7,
            winner_1_condition: 10,
            winner_2_condition: 9,
            winner_3_condition: 8,
            description: '',
            name: '',
            olympiad_type_id: 0,
            rules: '',
            subject: SubjectEnum.Physics
        }
        this.isCreated = false
    }

    create(): void
    {
        this.isCreated = true
        this.addClick.emit( this.createBaseOlympiadRequestTaskCreator )
    }

    isValid(): boolean
    {
        return true
    }

    onClick( $event: any ): void
    {
        if ( $event.target == this.modal?.nativeElement )
            this.modalVisible = false
    }
}
