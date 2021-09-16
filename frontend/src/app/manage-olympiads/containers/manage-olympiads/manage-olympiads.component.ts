import { Component, OnInit } from '@angular/core'
import { ManageOlympiadsStore } from '@/manage-olympiads/manage-olympiads.store'
import { Observable } from 'rxjs'
import { fixedHeight } from '@/shared/consts'
import { Contest, CreateBaseOlympiadRequestTaskCreator } from '@api/tasks/model'


@Component( {
    selector: 'app-manage-olympiads',
    templateUrl: './manage-olympiads.component.html',
    styleUrls: [ './manage-olympiads.component.scss' ],
    providers: [ ManageOlympiadsStore ]
} )
export class ManageOlympiadsComponent implements OnInit
{
    minContainerHeight: number = fixedHeight
    columnDefs = [
        { field: 'contest_id', sortable: true, filter: true, headerName: 'ID' },
        { field: 'description', sortable: true, filter: true, headerName: 'Описание' },
        { field: 'start_time', sortable: true, filter: true, headerName: 'Дата начала' },
        { field: 'end_time', sortable: true, filter: true, headerName: 'Дата окончания' },
        { field: 'rules', sortable: true, filter: true, headerName: 'Правила' },
        { field: 'winning_condition', sortable: true, filter: true, headerName: 'Условия победы' },
        { field: 'laureate_condition', sortable: true, filter: true, headerName: 'Условия лауреата' },
        { field: 'certificate_template', sortable: true, filter: true, headerName: 'Шаблон сертификата' },
        { field: 'visibility', sortable: true, filter: true, headerName: 'Видимость' }
    ]

    olympiads$: Observable<Contest[]> = this.store.contests
    addVisible: boolean = false

    constructor( private store: ManageOlympiadsStore ) {}

    ngOnInit(): void
    {
        this.store.reload()
    }

    getRowNodeId( data: Contest ): number | undefined
    {
        return data.contest_id
    }

    onAdd( createBaseOlympiadRequestTaskCreator: CreateBaseOlympiadRequestTaskCreator )
    {
        this.store.add( createBaseOlympiadRequestTaskCreator )
    }
}
